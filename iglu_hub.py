# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:10:57 2020

@author: Donald Wright
"""

import iglu_area
import iglu_hvac
import iglu_Timer
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
                
        self.__observers = []
        
        self.hvac = None
        
        self.addArea(name="Iglu Home", numSensor=1)
        
        #bind the update function to the clock
        iglu_Timer.globalTimer.bind_to(self.tick)
        
    #links callback funciton to a tag
    def bind_to_tag(self, tag, callback ):
        self.__observers.append( (tag,callback) )
    
    #Checks tag before calling callback funciton
    def runCallback( self, tag ):
        for entry in self.__observers:
            if tag in entry[0]:
                entry[1]()              

    def delete_bind_tag( self, tag ):
        for entry in self.__observers:
            if tag in entry[0]:
                del entry

    #Remove all bind calls
    # might need to add an additional filter flag to this
    def deleteAllBindings( self ):
        del self.__observers[:]
        for item in self.areaList:
            item.deleteAllBindings()

                
        
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
                                                    
            self.runCallback("addArea")
            return (self.areaList[-1])
        else:
            return None
    
    def getPrimaryArea( self ):
        if( len(self.areaList) > 0  ):
            return self.areaList[0]
        else:
            return None
            
    def setPrimaryArea( self, a ):
        if a in self.areaList:
            idx = self.areaList.index(a)
            tmp = self.areaList.pop(idx)
            self.areaList.insert(0, a)
            self.runCallback("primaryArea")

        
    def getSecondaryArea( self ):
        if( len(self.areaList) > 1  ):
            return self.areaList[1]
        else:
            return None
        
    def setSecondaryArea( self, a ):
        if a in self.areaList:
            idx = self.areaList.index(a)
            tmp = self.areaList.pop(idx)
            self.areaList.insert(1, a)
            self.runCallback("secondaryArea")
        

    def getTertiaryArea( self ):
        if( len(self.areaList) > 2  ):
            return self.areaList[2]
        else:
            return None
        
    def setTertiaryArea( self, a ):
        if a in self.areaList:
            idx = self.areaList.index(a)
            tmp = self.areaList.pop(idx)
            self.areaList.insert(2, a)
            self.runCallback("tertiaryArea")
        
    
    def delArea(self, a):
        if a in self.areaList:
            if len(self.areaList) > 1:
                self.areaList.remove(a)
                self.runCallback("delArea")
                return True
        else:
            return False
    
    def delAllArea(self):
        self.areaList.clear()
        self.runCallback("delAllArea")
        
    #####################################
    #  This is the main function which is 
    #    bound on __init__ to the global clock
    #
    #  This will trigger data collection
    #    and the responses for when that data is processed
    #
    #####################################
    def tick(self, newTimeValue):
       
        # Useful vars/methods
        # self.hvac.startCooling()     -- Method to put HVAC in A/C mode
        # self.hvac.startHeating()     -- Method to put HVAC in heating mode        
        # 
        # Measurements
        # self.hvac.exteriorTempature  -- This will dictate the general direction of temp trend should HVAC be off
        # a.currentTempature           -- This is the current measured tempature in an area
        # a.targetTempature            -- This is the current target tempature of an area
        # self.hvac.mode --- fixed?
        # a.activity                   -- This will heat the room, maybe take that into account when turning flow on/ or heating?
        
        # Adjustmets
        # self.hvac.mode               -- "Cooling"-1, "Heating"+1,"Standby"0
        # damperRate                   -- 100 full flow, 0 blocking
        
        
        numCold = 0;
        numHot = 0;
        
        coldSize = 0;
        hotSize = 0;
        
        trigThresh = .75
        
        #Update or collect information for each area        
        for a in self.areaList:
            for d in a.deviceList:
                if "updateSensors" in dir(d):
                    d.updateSensors()  #Gets new room readings
                    
            a.updateStats( newTimeValue ) #takes new room readings and gathers stats
            
            #collect decision making information
            if(a.currentTempature < a.targetTempature ):
                diff = (a.targetTempature - a.currentTempature)
                if( diff > trigThresh ):
                    numCold = numCold + 1
                    coldSize = coldSize + diff
            elif(a.currentTempature > a.targetTempature ): 
                diff = (a.currentTempature - a.targetTempature)
                if( diff > trigThresh ):
                    numHot = numHot + 1
                    hotSize = hotSize + diff
        
        #print( (numCold,numHot), (coldSize,hotSize))
        
        if( numCold > numHot or coldSize > hotSize):
            self.hvac.startHeating()
        elif( numCold < numHot or coldSize < hotSize):
            self.hvac.startCooling()
        elif( numCold == numHot and coldSize == hotSize):
            self.hvac.stop()
        
                  
    
if __name__=="__main__":
    hub = iglu_hub()
    counter = hub.device_counter
    areaID0 = hub.addArea();
    print(areaID0.name)
    areaID1 = hub.addArea();
    print(areaID1.name)
    areaID2 = hub.addArea();
    print(areaID2.name)

    hub.delArea(areaID2)
    hub.delArea(areaID0)


    
    #print(hub.areaList.name)
    
    
    