"""
Iglu Thermostat zone delimiter
Class for zone creation
Created by Donald Wright
11/13/20

Modified by: Brandon Lasher --  11/15/20
- Added decorators, and modified names
"""
import device
import iglu_Timer
import satelliteNode as SN
import damper as DA

zone_counter = 1100

class iglu_area:
    def __init__(self, name ="AREA NAME"):
        self.__name = name
        self.deviceList = []
        
        self.__currentTemp = 70
        self.__targetTemp = 70
        
        self.__currentHumidity = 45  #humidity level
        self.__targetHumidity = 45
        
        self.__currentCO = 0        #Carbon monoxide levels
        self.__targetCO = 0
        
        self.__currentActivity = 0  #motion in room
        
        #used for simulation purposes
        # combined with HVAC info will determine how fast the room cools or heats
        self.__sqft = 500
        self.__rValue = 20
        
        self.__lastTimeStamp = None
        
        self.__observers = []
        
        self.__rank = None
        
        #Simulation properties
        self.__currentTempatureActual = 70
        self.__currentHumidityActual = 45  
        self.__currentCOActual = 45 
        self.__currentActivityActual = 0
        
        self.__extRateChange =  0  # Abs Rate of change of the currentTempature due to exterior Temp
        self.__hvacRateChange = 0  # Abs rate of change of the currentTempature doue HVAC ( will adjust sign based on Mode)
        
        self.extRateSign =  0  # If hotter outside: "+1", if colder outside: "-1"
        self.hvacMode = 0  # If heating: "+1", if cooling outside: "-1", if standby: 0
    
        
    #links callback funciton to a tag
    def bind_to_tag(self, tag, callback ):
        self.__observers.append( (tag,callback) )
    
    #Checks tag before calling callback funciton
    def runCallback( self, tag ):
        for entry in self.__observers:
            if tag in entry[0]:
                entry[1]()              

    #Remove all bind calls
    # might need to add an additional filter flag to this
    def delete_bind_tag( self, tag ):
        for entry in self.__observers:
            if tag in entry[0]:
                del entry

    #Remove all bind calls
    # might need to add an additional filter flag to this
    def deleteAllBind( self ):
        del self.__observers[:]
    
    #functions to modify or change name
    @property
    def name(self):
       return self.__name

    @name.setter
    def name(self, newName):
        self.__name = newName
        self.runCallback( "name")
        
    #functions to modify or change name
    @property
    def rank(self):
       return self.__rank

    @rank.setter
    def rank(self, newRank):
        self.__rank = newRank
        self.runCallback( "rank")
        
    def updateStats(self, timestamp):
        if not( timestamp == self.__lastTimeStamp ):  
            sensorData = [0]*4;          
            sensorCnt = 0;
            self.__lastTimeStamp = timestamp
            
            for d in self.deviceList:
                if isinstance( d, SN.satelliteNode ):
                    sensorCnt = sensorCnt + 1
                    
                    #
                    #  Can't easily loop over all of them as one loop
                    #   because they are combined differently
                    #
                    #Average Temp over history?
                    iterLen = min(len( d.sensors[0]["history"] ),5 )
                    sum = 0;
                    for h in range(0,iterLen):
                        sum += d.sensors[0]["history"][-1-h][1]                        
                    sensorData[0] = sensorData[0] + (sum/iterLen if iterLen>0 else 0)           #Temp
                        
                    sensorData[1] = sensorData[1] and d.sensors[1]["history"][-1][1]            #Activity
                    sensorData[2] = sensorData[2] + d.sensors[2]["history"][-1][1]              #Humiditiy
                    sensorData[3] = max( sensorData[3], d.sensors[3]["history"][-1][1] )        #CO
                 
            if( sensorCnt >  0):
                self.currentTempature = sensorData[0] / sensorCnt
                self.currentHumidity = sensorData[2] / sensorCnt
                self.activity = sensorData[1]
                self.carbonMonoxide = sensorData[3]            



    #functions tomodify or change temperature
    @property
    def currentTempature(self):
        return self.__currentTemp
    
    @currentTempature.setter
    def currentTempature(self, newTemp):
        self.__currentTemp = newTemp
        self.runCallback( "currentTempature")
        
    @property
    def targetTempature(self):
        return self.__targetTemp
    
    @targetTempature.setter
    def targetTempature(self, newTemp):
        self.__targetTemp = newTemp
        self.runCallback( "targetTempature")
        
    #functions to modify humidity levels
    @property
    def currentHumidity(self):
        return self.__currentHumidity
    
    @currentHumidity.setter
    def currentHumidity(self, newHumidity):
        self.__currentHumidity = newHumidity
        #[ d.setMeanHumidity( self.currentHumidity ) for d in self.deviceList if isinstance(d, SN.satelliteNode)]
        self.runCallback("currentHumidity")
        
    #functions to modify humidity levels
    @property
    def targetHumidity(self):
        return self.__targetHumidity
    
    @targetHumidity.setter
    def targetHumidity(self, newHumidity):
        self.__targetHumidity = newHumidity
        self.runCallback("targetHumidity")
        
    #function to modify human activity
    @property
    def activity(self):
        return self.__currentActivity
    
    @activity.setter
    def activity(self, newActivity):
        self.__currentActivity = newActivity
        #[ d.setMeanActivity( self.activity ) for d in self.deviceList if isinstance(d, SN.satelliteNode)]
        self.runCallback("activity")
        
    #function to modify CO level
    @property
    def carbonMonoxide(self):
        return self.__currentCO
    
    @carbonMonoxide.setter
    def carbonMonoxide(self, newCO):
        self.__currentCO = newCO
        self.runCallback("carbonMonoxide")       
        
    @property
    def externalTempatureChangeRate( self ):
        return self.__extRateChange
    
    @externalTempatureChangeRate.setter
    def externalTempatureChangeRate( self, newRate ):
        self.__extRateChange = newRate
        self.runCallback("externalTempatureChangeRate")
    
    @property
    def hvacTempatureChangeRate( self ):
        return self.__hvacRateChange
    
    @hvacTempatureChangeRate.setter
    def hvacTempatureChangeRate( self, newRate ):
        self.__hvacRateChange = newRate
        self.runCallback("hvacTempatureChangeRate")
    
    
    #function to add/delete devices
    def addDevice(self, device):
        self.deviceList.append(device)
        
        if isinstance(device, SN.satelliteNode ):
            pass #setup sensor values
        
            
        return self.deviceList[-1]
    
    @property
    def currentTempatureActual( self ):
        return self.__currentTempatureActual
    
    @currentTempatureActual.setter
    def currentTempatureActual( self, newTemp ):
        self.__currentTempatureActual = newTemp
        [ d.setMeanTempature( self.__currentTempatureActual ) for d in self.deviceList if isinstance(d, SN.satelliteNode)]
        self.runCallback("currentTempatureActual")    
    
    #Will update the Actual Tempature of the room
    def updateCurrentTemp( self ):
        #Get overall flow Rate
        rates = [d.flowRate for d in self.deviceList if isinstance( d, DA.damper )] 
        avgFlowRate = (sum(rates)/len(rates))/100 if len(rates) > 0 else 1

        #get change due to each factor        
        changeExt = (self.externalTempatureChangeRate * self.extRateSign)
        changeHvac = self.hvacMode*(self.hvacTempatureChangeRate*avgFlowRate)
        
        self.currentTempatureActual = self.currentTempatureActual  + changeExt + changeHvac

if __name__=="__main__":
    
    a = iglu_area()
    print(a.name)
    print("Current temperature: ", a.currentTempature)
    print("Current Humdiity: ", a.currentHumidity, "%")
    print("Room Occupancy: ", a.activity)
    print("CO level: ", a.carbonMonoxide, "ppm")
    a.name = "Living Room"
    a.currentTempature  = 75
    a.currentHumidity = 53
    a.activity = "Occupied"
    a.carbonMonoxide = 1.2
    print(a.name)
    print("Current temperature: ", a.currentTempature)
    print("Current Humdiity: ", a.currentHumidity, "%")
    print("Room Occupancy: ", a.activity)
    print("CO level: ", a.carbonMonoxide, "ppm")
    
    print()


    
    
    
    