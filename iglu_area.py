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
        
    def updateStats(self):
        cnt = 0
        tempValue = 0
        humidityValue = 0
        active = 0;
        ppmValue = 0;
        for d in self.deviceList:
            if isinstance( d, SN.satelliteNode ):
                u = d.getLastUpdate()
                
                #if a valid element
                if( u["Thermometer"][0] ):
                    
                    #if the timestamp is new update
                    if not( self.__lastTimeStamp == u["Thermometer"][0][0] ):
                        self.__lastTimeStamp = u["Thermometer"][0][0] 
                        
                        tempValue = tempValue + u["Thermometer"][0][1]
                        humidityValue = humidityValue + u["Hygrometer"][0][1]
                        active = active or u["PersonDetector"][0][1]
                        ppmValue = max(ppmValue, u["CarbonMonoxide"][0][1] )
                        cnt + cnt + 1

                        self.currentTempature = tempValue / max(cnt,1)
                        self.currentHumidity = humidityValue / max(cnt,1)
                        self.activity = active
                        self.carbonMonoxide = ppmValue
                       
                    else:
                        break;
                    


    #functions tomodify or change temperature
    @property
    def currentTempature(self):
        self.updateStats()
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
        self.updateStats()
        return self.__currentHumidity
    
    @currentHumidity.setter
    def currentHumidity(self, newHumidity):
        self.__currentHumidity = newHumidity
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
        self.updateStats()
        return self.__currentActivity
    
    @activity.setter
    def activity(self, newActivity):
        self.__currentActivity = newActivity
        
    #function to modify CO level
    @property
    def carbonMonoxide(self):
        self.updateStats()
        return self.__currentCO
    
    @carbonMonoxide.setter
    def carbonMonoxide(self, newCO):
        self.__currentCO = newCO
        
        
    #function to add/delete devices
    def addDevice(self, device):
        self.deviceList.append(device)
        return self.deviceList[-1]


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


    
    
    
    