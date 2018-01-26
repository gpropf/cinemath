#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import threading
import turtle

sys.path.append("../")
import Spiderbrot


## Git test - ignore 3

turtleBoxCorner = 1

Spiderbrot.angleStep = 60
Spiderbrot.jerkThreshold = 5.6e-5
turtle.setworldcoordinates(-turtleBoxCorner,-turtleBoxCorner,turtleBoxCorner,turtleBoxCorner)
Spiderbrot.makeMovieFrames(0, 10000, 1000, "spbif4")
