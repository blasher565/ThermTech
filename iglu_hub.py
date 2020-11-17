# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:10:57 2020

@author: Donald Wright
"""

import iglu_area
import device
import satelliteNode as SN
import damper as DA



class iglu_hub:
    def __init__(self):
        self.areaList = []
        self.deviceList = []
        self.device_counter = 1000
        self.areaCounter = 0
        self.maxNumAreas = 4
        
        self.sensorID = 1000 #keeps track of the next sensor ID
        self.damperID = 2000 #keeps track of the next damper ID
        
    def addArea(self, name=None, numSensor = 0, numDamper = 0 ):
            
        if( self.maxNumAreas > (len(self.areaList)) ):
            
            if not name:
                name = "Area " + str(self.areaCounter)
                
            self.areaList.append(iglu_area.iglu_area( name=name ) )
            self.areaCounter  = self.areaCounter+1
            
            for n in range(numSensor):
                self.areaList[-1].addDevice( SN.satelliteNode( name =  name + str(self.sensorID) , uniqueID= self.sensorID ) )
                self.sensorID=self.sensorID+1
            
            for n in range(numDamper):
                self.areaList[-1].addDevice( DA.damper( name =  name + str(self.sensorID) , uniqueID= self.damperID ) )
                self.damperID=self.damperID+1
            
            return (self.areaList[-1])
        else:
            return None
    
    def delArea(self, a):
        if a in self.areaList:
            self.areaList.remove(a)            
            return True
        else:
            return False
    
    def delAllArea(self):
        self.areaList.clear()
                  
    
if __name__=="__main__":
    hub = iglu_hub()
    counter = hub.device_counter
    areaID0 = hub.addArea();
    print(areaID0.name)
    areaID1 = hub.addArea();
    print(areaID1.name)
    areaID2 = hub.addArea();
    print(areaID2.name)
    areaID3 = hub.addArea();
    print(areaID3.name)


    hub.delArea(areaID2)
    hub.delArea(areaID0)
    
    
    areaID = hub.addArea();
    print(areaID)
    print()
       

    
    #print(hub.areaList.name)
    
    
    