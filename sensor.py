#!/usr/bin/env python3

"""
Author: Brandon Lasher

Contains the implentation for a basic sensor 

"""

import random
#from datetime import datetime
import iglu_Timer


class sensor():
    def __init__(self, sensorType, mu=10, std=1, bias=0):
        self.sensorType = sensorType
        self.meanValue = mu
        self.variance = std
        self.bias = bias


    def __repr__(self):
        return self.sensorType

    # returns new sensor data
    # in reality would query the hardware
    def getUpdate( self ):
        return (iglu_Timer.globalTimer.absTime.isoformat(), round(random.gauss(self.meanValue + self.bias, self.variance), 2))
        #return (iglu_Timer.globalTimer.absTime.isoformat(), round(random.randint(0,10), 2))

