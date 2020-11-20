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
from random import gauss


class satelliteNode( device ):
    def __init__( self, name, uniqueID ):
        device.__init__( self, name, uniqueID, "satelliteNode" )
                
        self.sensors = {
                  0 : { "sensor" : sensor( "Tempature", mu=70, std=.05, bias=gauss(0,.1) ), "formatText": u"{}\N{DEGREE SIGN} F", "history": [] },     #Tempature
                  1 : { "sensor" : sensor( "Activity", mu=0, std=10, bias=0 ),  "formatText": u"{}", "history": [] },       #Infrared? Person in room?
                  2 : { "sensor" : sensor( "Humidity", mu=40, std=.5, bias=gauss(0,.2)  ),  "formatText": u"{} %", "history" : [] },                   #Humidity
                  3 : { "sensor" : sensor( "C0", mu=2, std=.1, bias=gauss(0,.2) ),  "formatText": u"{} PPM", "history": [] }     #Carbon Monoxide
                }
        
        self.maxHistorySize = 10
        
    #print function
    def __repr__(self):
        out = "Name: {}, Type: {}, UUID: {}\n".format(  self.name, str(self.deviceType), str( self.uniqueID ))
        for k1, v1 in self.sensors.items():
            out += "[{}]\n-----------\n{}\n\n".format(str( v1["sensor"] ),  "\n".join(map(str, v1["history"])))
        return out;

    def setMeanTempature(self, value):
        self.sensors[0]["sensor"].meanValue = value
    
    def setMeanHumidity(self, value):
        self.sensors[2]["sensor"].meanValue = value
    
    def setMeanActivity(self, value):
        self.sensors[1]["sensor"].meanValue = value
    
    def setMeanCarbonMonoxide(self, value):
        self.sensors[3]["sensor"].meanValue = value    

    #Simple Call to update the sensor and add it to the history
    def updateSensors( self, index=-1 ):
        if( index == -1 ):
            for k1, v1 in self.sensors.items():
                
                if len( v1["history"] ) >= self.maxHistorySize:
                    del v1["history"][0]
                    
                v1["history"].append( v1["sensor"].getUpdate() )
        else:
            if index in self.sensors:
                self.sensors[index]["history"].append( self.sensors[index]["sensor"].getUpdate() )
            else:
                pass
        
        self.updateObservers()
    
    def getLastUpdate( self ):
        out = {}
        for k1, v1 in self.sensors.items():
            if( len(v1["history"]) > 0 ):
                out[ str(v1["sensor"]) ] = ( v1["history"][-1], v1["formatText"])
            else:
                out[ str(v1["sensor"])  ] = ( None, v1["formatText"])
        return out


if __name__ == "__main__" :
  s=satelliteNode("bob", 1234 )
  s.updateSensors()
  sleep(1)
  s.updateSensors()
  sleep(1)
  s.updateSensors(0)
  sleep(1)
  s.updateSensors(8)

  print( s )
  
  print( s.getLastUpdate() )





