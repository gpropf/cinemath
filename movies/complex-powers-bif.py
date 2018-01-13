#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import threading
import turtle

sys.path.append("../")
import Spiderbrot


## Git test - ignore

turtle.setworldcoordinates(-3,-3,3,3)
Spiderbrot.makeParallelMovie(0, 10000, 1000, "spbif4", 2)
