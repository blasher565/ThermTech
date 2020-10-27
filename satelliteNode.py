#!/usr/bin/env python3

"""
Author: Brandon Lasher

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
                  0 : { "sensor" : sensor( "Thermometer" ) , "history": [] },     #Tempature
                  1 : { "sensor" : sensor( "PersonDetector" ) , "history": [] },  #Infrared? Person in room?
                  2 : { "sensor" : sensor( "Hygrometer" ) , "history": [] },      #Humidity
                  3 : { "sensor" : sensor( "CarbonMonoxide"), "history": [] }     #Carbon Monoxide
                }

    #print function
    def __repr__(self):
        out = "Name: {}, Type: {}, UUID: {}\n".format(  self.getName(), str(self.getDeviceType()), str( self.getUniqueID()  ))
        for k1, v1 in self.sensors.items():
            out += "[{}]\n-----------\n{}\n\n".format(str( v1["sensor"] ),  "\n".join(map(str, v1["history"])))
        return out;

    #Simple Call to update the sensor and add it to the history
    def updateSensors( self, index=-1 ):
        if( index == -1 ):
            for k1, v1 in self.sensors.items():
                v1["history"].append( v1["sensor"].getUpdate() )
        else:
            if index in self.sensors:
                self.sensors[index]["history"].append( self.sensors[index]["sensor"].getUpdate() )
            else:
                pass



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





