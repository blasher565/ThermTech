#!/usr/bin/env python3

"""
Author: Brandon Lasher

Contains the implentation for a basic sensor 

"""

import random
#from datetime import datetime
import iglu_Timer


class sensor():
    def __init__(self, sensorType):
        self.sensorType = sensorType

    def __repr__(self):
        return self.sensorType

    # returns new sensor data
    # in reality would query the hardware
    def getUpdate( self ):
        return (iglu_Timer.globalTimer.absTime.isoformat(), random.randint(0,10))


