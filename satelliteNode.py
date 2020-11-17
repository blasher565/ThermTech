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


class satelliteNode( device ):
    def __init__( self, name, uniqueID ):
        device.__init__( self, name, uniqueID, "satelliteNode" )
                
        self.sensors = {
                  0 : { "sensor" : sensor( "Thermometer" ), "formatText": u"{}\N{DEGREE SIGN} F", "history": [] },     #Tempature
                  1 : { "sensor" : sensor( "PersonDetector" ),  "formatText": u"{}", "history": [] },       #Infrared? Person in room?
                  2 : { "sensor" : sensor( "Hygrometer" ) ,  "formatText": u"{} %", "history" : [] },                   #Humidity
                  3 : { "sensor" : sensor( "CarbonMonoxide"),  "formatText": u"{} PPM", "history": [] }     #Carbon Monoxide
                }
        
        self.maxHistorySize = 50
        
    #print function
    def __repr__(self):
        out = "Name: {}, Type: {}, UUID: {}\n".format(  self.name, str(self.deviceType), str( self.uniqueID ))
        for k1, v1 in self.sensors.items():
            out += "[{}]\n-----------\n{}\n\n".format(str( v1["sensor"] ),  "\n".join(map(str, v1["history"])))
        return out;

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
                out[ v1["sensor"]  ] = ( v1["history"][-1], v1["formatText"])
            else:
                out[ v1["sensor"]  ] = ( None, v1["formatText"])
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





