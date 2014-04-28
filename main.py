#!/usr/bin/python

from rpi_libs.led import Led


l = Led("led 7", 7)
l.blink_n()
l.blink()

