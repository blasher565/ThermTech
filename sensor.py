#!/usr/bin/env python3

"""
Author: Brandon Lasher

Contains the implentation for a basic sensor 

"""

import random
from datetime import datetime

class sensor():
    def __init__(self, sensorType):
        self.sensorType = sensorType

    def __repr__(self):
        return self.sensorType

    # returns new sensor data
    # in reality would query the hardware
    def getUpdate( self ):
        return (datetime.now().isoformat(), random.randint(0,10))


