#!/usr/bin/env python3

"""
Author: Brandon Lasher
Secondary: Christian Wagner (Last Update: 11/02/2020)

Contains the implentation for a satellite Node
   A satellite Node contains sensors which feed back in
   to the hub. 

"""


from device import device
from time import sleep
from sensor import sensor
import random 


class damper( device ):
    def __init__( self, name, uniqueID ):
        device.__init__( self, name, uniqueID, "damper" )
        self.__flowRate = float(100); #in percent
    

    #print function
    def __repr__(self):
        out = "Name: {}, Type: {}, UUID: {}\n".format(  self.name, str(self.deviceType), str( self.uniqueID ))
        out += "[{}]\n-----------\n{}{:.1f}{}\n\n".format(self.deviceType,   "Flow Rate: ", self.flowRate, " %" )
        #out += "[{}]\n-----------\n{}\n\n".format(str( v1["sensor"] ),  "\n".join(map(str, v1["history"])))
        return out;
    
    @property
    def flowRate( self ):
        return self.__flowRate;
    
    @flowRate.setter
    def flowRate( self, rate ):
        self.__flowRate = rate;
        self.updateObservers()        
        return rate;
        
    def updateSensors( self ):
        pass
 

if __name__ == "__main__" :
  s=damper("bob", 1234 )

  out = str(s)
  print( out )






