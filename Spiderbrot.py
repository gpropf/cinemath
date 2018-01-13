#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#from Tkinter import *

from turtle import *
from random import *
from math import *
from cmath import *
import os
from PIL import Image, ImageDraw

import threading


bkgColor = "white"
windowWidth = 4100
windowHeight = 4000
captionCircleRadius = 20
maxIterations = 200
bifurcationAngle = 0.5
jerkThreshold = 0.0005

setup(windowWidth,windowHeight)

caption_x = -(windowWidth / 2 - captionCircleRadius * 2)
caption_y = windowHeight / 2 - captionCircleRadius * 2


bgcolor("black")
delay(0)

speed(0)
tracer(False)

# These two factors are the "sweet spot", producting
# drawings that are just about the right size.
initialVelocityScaleFactor = 0.005
accelerationScalingFactor=0.001

# This prevents us from moving by huge amounts and producing that
# "spider leg" effect that led to my original name for this program. The
# idea is to scale the simulated time down if the speed is large to keep
# the spatial resolution of the patterns high.
maxPositionChangePerIteration = 0.02

setworldcoordinates(-2,-2,2,2)


def bifurcateVector(v,alpha):
    (vr,vtheta) = polar(v)
    v1 = rect(vr,vtheta-alpha)
    v2 = rect(vr,vtheta+alpha)
    return (v1,v2)
    


# Keeps us from plotting too far into the generally boring regions
# beyond a few units from the origin.
maxDistanceFromOrigin = 2

def makeTrack(drawingCb,completedCb, accelCb=(lambda p: p**2),
              initialPosition=(0+0j),
              initialVelocity=(initialVelocityScaleFactor +
                               initialVelocityScaleFactor*1j),              
              windowScaleFactor=1,dragCoefficient=0,remainingRecursions=2):
    """ makeTrack:
    drawingCb: callback to draw the current position
    completedCb: callback to decide whether to terminate the current track
    accelCb: callback to calculate the new acceleration based on position.
    initialPosition: complex valued start position
    initialVelocity: complex valued initial velocity, specifies the vector we
                     start off in.
    windowScaleFactor: the values of p,v,a,and j are in terms of positions in the complex plane.
                       generally, these are small values between the rectangle whose upper left
                       and lower right corners are at -2-2j and 2+2j, respectively. These values
                       are too small to plot so we scale the plot accordingly. A value of 500
                       here is a good rule of thumb.
    dragCoefficient: This isn't a true drag coefficient but is subtracted
                     from 1 to get the multiplier we use per iteration for v.
                     Basically, larger values make the projectile slow down faster.
                     Use 0 for frictionless movement."""
    if remainingRecursions == 0:
        return
    hideturtle()
    timeScaleFactor = 1
    p_init = p = initialPosition
    v = initialVelocity
    a = 0+0j
    j = 0+0j
    d = 1 - dragCoefficient
    i = 0
    #print("initial vel:" + str(v))
    penup()
    goto(initialPosition.real*windowScaleFactor,initialPosition.imag*windowScaleFactor)
    pendown()
    tracer(0)
    while(not completedCb(i,p - p_init,v,a,j,maxIterations)):
        drawingCb(i,p*windowScaleFactor,v,a,j)
        old_a = a
        a = accelerationScalingFactor * accelCb(p)
        j = a - old_a
#        print ("Jerk = " + str(abs(j)))
        v = v + a
        v = v * d
        newTSF = maxPositionChangePerIteration/abs(v)
        timeScaleFactor = newTSF if (newTSF < 1) else 1
        if abs(j) > jerkThreshold and i != 1:
            i = maxIterations + 1
            (v1,v2) = bifurcateVector(v,bifurcationAngle)
            (v11,v12) = bifurcateVector(v1,bifurcationAngle/2)
            (v21,v22) = bifurcateVector(v2,bifurcationAngle/2)

            for vbif in [v11,v12,v21,v22]:
            
                makeTrack(drawingCb,completedCb, accelCb=accelCb,
                          initialPosition=p,
                          initialVelocity=vbif,              
                          windowScaleFactor=1,dragCoefficient=0,remainingRecursions = remainingRecursions - 1)
    
        p = p + v * newTSF       
        i = i + 1
    penup()
            
    #showturtle()
    
def dcb(i,p,v,a,j):
    newTSF = maxPositionChangePerIteration/abs(v)
    timeScaleFactor = newTSF if (newTSF < 1) else 1
    abs_a = abs(a)
    
    #green = 0 if (abs_a == 0 or log(abs_a) == 0) else 1 - 1/abs(log(abs_a))
    #max_p_size = 15
    #p_size = max_p_size - (green * max_p_size)
    pensize(2)
    #print("Green: " + str(green))
    color((1-timeScaleFactor,0,timeScaleFactor))
    goto(p.real,p.imag)

def ccb(i,p,v,a,j,maxiter):
    """ ccb: Standard completion test, keeps the iteration count
        reasonable and the size limited in radius. """
    
    if i < maxiter and abs(p) < maxDistanceFromOrigin:
        return False
    else:
        return True


def makeBoxAtCenter(cornerCoord):
    penup()
    goto(-cornerCoord,-cornerCoord)
    pendown() 
    goto(cornerCoord,-cornerCoord)
    goto(cornerCoord,cornerCoord)
    goto(-cornerCoord,cornerCoord)
    goto(-cornerCoord,-cornerCoord)
    penup()
    
def drawSpider(accelCb=(lambda p: p**2)):
    """ drawSpider: single argument is the callback that computes the
    acceleration from p, the position. """

    pensize(0.5)
    tracer(False)
    clear()
    
    for x in range(-3,4):
        for y in range(-3,4):
            for theta in range(0,360,60):
                thetaRads = theta*(2*pi/360)
                iv = cos(thetaRads) + sin(thetaRads) * 1j
                iv = iv * initialVelocityScaleFactor
                iv = iv * 0.5
                #penup()
                #goto(0,0)
                 
#                penup()
                
                
               
                ##    makeTrack(drawingCb=dcb,completedCb=ccb,initialVelocity=iv,
                ##              windowScaleFactor=0.5)
                makeTrack(accelCb=accelCb, drawingCb=dcb,completedCb=ccb,
                          windowScaleFactor=1,initialPosition=(x+y*1j),
                          initialVelocity=iv,
                          dragCoefficient=0.0)
#                tracer(True)
                penup()



def drawSpiderBifurcate(accelCb=(lambda p: p**2)):
    """ drawSpider: single argument is the callback that computes the
    acceleration from p, the position. """
    x = y = 0
    pensize(0.5)
    tracer(False)
    clear()
    for theta in range(30,360,60):
        thetaRads = theta*(2*pi/360)
        iv = cos(thetaRads) + sin(thetaRads) * 1j
        iv = iv * initialVelocityScaleFactor
        iv = iv * 0.5
        makeTrack(accelCb=accelCb, drawingCb=dcb,completedCb=ccb,
                  windowScaleFactor=1,initialPosition=(x+y*1j),
                  initialVelocity=iv,
                  dragCoefficient=0.0)
        #                tracer(True)
        penup()

                #penup()
                #goto(0,0)
                 
#                penup()
                
                
               
                ##    makeTrack(drawingCb=dcb,completedCb=ccb,initialVelocity=iv,
                ##              windowScaleFactor=0.5)
                

def makeMovie(startPower, endPower, stepsPerPower, baseFilename, startFrame = 0):
    endPower = endPower * stepsPerPower 
    startPower = startPower * stepsPerPower
    frameCount = startFrame
    baseFilename = "NOSYNC/" + baseFilename
    for n in map(lambda x: x/float(stepsPerPower),
                 range(int(startPower),int(endPower) + 1)):

        tracer(0,0)
        hideturtle()
        drawSpiderBifurcate((lambda p: p**n))

        update()
        fileIndexStr = str(frameCount).zfill(6)
        cv = getscreen().getcanvas()
        cv.pack()
        filename = baseFilename + "_" + fileIndexStr
        psFileName = filename + ".ps"
        cv.postscript(file=psFileName,
                      colormode='color', rotate='0')
        
        shellCmd = "pstopnm -ysize 4000 -xsize 4100 {0}.ps -stdout | ppmchange '#ffffff' '#000000' | pnmrotate -90 | ppmtojpeg >{0}.jpg".format(filename) 
        print(shellCmd)
        os.system(shellCmd)
        os.remove(psFileName)
        
        print("n:"+str(n))
        frameCount = frameCount + 1

        
def makeMovieFrames(startFrame, endFrame, framesPerPower, baseFilename):
    baseFilename = "NOSYNC/" + baseFilename
    tracer(0,0)
    hideturtle()

    for frame in range(startFrame, endFrame):
        n = frame / framesPerPower
        drawSpiderBifurcate((lambda p: p**n))
        update()
        fileIndexStr = str(frame).zfill(6)
        cv = getscreen().getcanvas()
        cv.pack()
        filename = baseFilename + "_" + fileIndexStr
        psFileName = filename + ".ps"
        cv.postscript(file=psFileName,
                      colormode='color', rotate='0')
        
        shellCmd = "pstopnm -ysize 4000 -xsize 4100 {0}.ps -stdout | ppmchange '#ffffff' '#000000' | pnmrotate -90 | ppmtojpeg >{0}.jpg".format(filename) 
        print(shellCmd)
        os.system(shellCmd)
        os.remove(psFileName)
        print("n = " + str(n) + ", frame = " + str(frame))

        


def makeParallelMovie(startFrame, endFrame, framesPerPower, baseFilename, cpus=1):
    """ Does not, in fact, mave the movie in parallel. Using Tk in parallel
    is apparently more trouble than it's worth. """
    
#    powerRange = endPower - startPower
#    totalFrames = powerRange * framesPerPower
    framesPerCPU = int(endFrame / cpus)

    cpu = 0
#    threads = []
    for cpuStartFrame in range(0,endFrame,framesPerCPU):
#        t = threading.Thread(target = makeMovieFrames, args = [cpuStartFrame, cpuStartFrame + framesPerCPU, framesPerPower, baseFilename])
        print("CPU = " + str(cpu) + ", startFrame = " + str(cpuStartFrame))
        cpu = cpu + 1
#        threads.append(t)
#        t.start()
        makeMovieFrames(cpuStartFrame, cpuStartFrame + framesPerCPU, framesPerPower, baseFilename)
    
        
    
