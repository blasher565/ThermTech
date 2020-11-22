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
        
        self.addArea(name="Iglu Home", numSensor=1, numDamper=1)
        
        #bind the update function to the clock
        iglu_Timer.globalTimer.bind_to(self.tick)
        
        self.lastTickTimeStamp = -10
        
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

        """
        # 
        # Christian's Implementation
        #
        
        size = len(self.areaList)
        tempMax = -1000;        
        tempMaxDiff = -1000;        
        tempDiff = [0]*size
        
        extRmax = -1000
        extRValue = [0]*size
        
        if( self.hvac.fanOn ):
            threshDiff = .5
        else:
            threshDiff = 2
        
        for i,a in enumerate(self.areaList):
            for d in a.deviceList:
                if "updateSensors" in dir(d):
                    d.updateSensors()  #Gets new room readings
                    
            a.updateStats( newTimeValue ) #takes new room readings and gathers stats
            
            tempMax = max(tempMax, a.currentTempature)
            tempDiff[i] = (a.targetTempature - a.currentTempature)
            tempMaxDiff = max(tempMaxDiff, tempDiff[i] )
            
            extRmax = max(extRmax, a.externalTempatureChangeRate)
            extRValue[i] = a.externalTempatureChangeRate

        
        
        #Setup HVAC mode
        m = 0
        for i in range(0,len(self.areaList)):
            m = m + (tempDiff[i] * extRValue[i]) / (size * extRmax)
        
        print( m )
        
        if( m < -threshDiff ):
            self.hvac.startCooling()
        elif( m > threshDiff ):
            self.hvac.startHeating()
        else:
            self.hvac.stop()
            
        #Setup dampers
        for i, a in enumerate(self.areaList):
            flowRate = abs(tempDiff[i]) / abs(tempMaxDiff) if tempMaxDiff != 0 else 1 
            for d in a.deviceList:
                if isinstance(d, DA.damper):
                    d.flowRate = flowRate
        """    
        
        
        
        #
        # Brandon's Simplistic Implementation
        #
        
        numCold = 0;
        numHot = 0;
        
        coldSize = 0;
        hotSize = 0;
        
        trigThresh = 1
        minTimeDiff = 10 
        
        #( 0 = OFF, 1=Heat Only, 2=Cool Only, 3=Auto )
        print (self.hvac.opMode)
        canCool = (self.hvac.opMode == 2) or (self.hvac.opMode == 3)
        canHeat = (self.hvac.opMode == 1) or (self.hvac.opMode == 3)
        
        #check for bad mode setting
        #  Ignore the timers?
        if (self.hvac.opMode == 2 and self.hvac.mode == 1) or ( self.hvac.opMode == 1 and self.hvac.mode == -1 ):
            self.hvac.stop()
        
        
        for i,a in enumerate(self.areaList):
            for d in a.deviceList:
                if "updateSensors" in dir(d):
                    d.updateSensors()  #Gets new room readings
                    
            a.updateStats( newTimeValue ) #takes new room readings and gathers stats
        
        
        #Update or collect information for each area        
        maxColdDiff = 0
        maxHotDiff = 0
        for a in self.areaList:
            
            #collect decision making information
            diff = a.currentTempature - a.targetTempature
            if(diff < 0 ):
                maxColdDiff = max(maxColdDiff, abs(diff))
                if( abs(diff) > trigThresh ):
                    numCold = numCold + 1
                    coldSize = coldSize + abs(diff)
            elif(diff > 0):                 
                maxHotDiff = max(maxHotDiff, abs(diff))
                if( abs(diff) > trigThresh ):
                    numHot = numHot + 1
                    hotSize = hotSize + abs(diff)

        #only allow change after minTimeDiff has passed
        if( (newTimeValue - self.lastTickTimeStamp) >  minTimeDiff ):
            self.lastTickTimeStamp = newTimeValue
            
            #print( (numCold,numHot), (coldSize,hotSize))
            avgCold = (coldSize/max(1,numCold))
            avgHot = (hotSize/max(1,numHot))
            
            if(( numCold > numHot or  avgCold > avgHot) and canHeat ):
                self.hvac.startHeating()
            elif(( numCold < numHot or avgCold < avgHot) and canCool ):
                self.hvac.startCooling()
            elif( numCold == numHot and avgCold == avgHot):
                self.hvac.stop()
            else:
                #print("I DON'T KNOW WHAT TO DO!!!!!")
                pass
        
                
        #iterate again and check dampers?
        for a in self.areaList:
            #collect decision making information
            diff = a.currentTempature - a.targetTempature 
            if(( diff > 0 and self.hvac.mode == 1) or    # need cooling, but is heating,
               ( diff < 0 and self.hvac.mode == -1) ):   # need heating, but is cooling,
                #print( f"{a.name}  needs OPPOSITE OF HVAC")
                for d in a.deviceList:
                    if isinstance(d, DA.damper):
                        d.flowRate = 0
            elif( diff > 0 and self.hvac.mode == -1 ): #need cooling and is cooling
                #print( f"{a.name} needs COOLING and HVAC is COOLING ")
                for d in a.deviceList:
                    if isinstance(d, DA.damper):
                        d.flowRate = max(.20, abs(diff)/maxHotDiff ) * 100
            elif( diff < 0 and self.hvac.mode == 1 ): #need heating and is heating
                #print( f"{a.name} needs HEATING and HVAC is HEATING")
                for d in a.deviceList:
                    if isinstance(d, DA.damper):
                        d.flowRate = max(.20, abs(diff)/maxColdDiff ) * 100
            elif( self.hvac.mode == 0 ):  
                #print( f"{a.name} OPEN HVAC in Standby ")
                for d in a.deviceList:
                    if isinstance(d, DA.damper):
                        d.flowRate = 100
        
    
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
    
    
    