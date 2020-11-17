"""
Iglu Thermostat zone delimiter
Class for zone creation
Created by Donald Wright
11/13/20

Modified by: Brandon Lasher --  11/15/20
- Added decorators, and modified names
"""
import device
zone_counter = 1100

class iglu_area:
    def __init__(self, name ="AREA NAME"):
        self.__name = name
        self.deviceList = []
        
        self.__currentTemp = 0
        self.__targetTemp = 0
        
        self.__currentHumidity = 0  #humidity level
        self.__targetHumidity = 0
        
        self.__currentCO = 0        #Carbon monoxide levels
        self.__targetCO = 0
        
        self.__currentActivity = "Empty"  #motion in room
        self.__targetActivity = 0
        
        #used for simulation purposes
        # combined with HVAC info will determine how fast the room cools or heats
        self.__sqft = 500
        self.__rValue = 20
    
    #functions to modify or change name
    @property
    def name(self):
       return self.__name

    @name.setter
    def name(self, newName):
        self.__name = newName

    #functions tomodify or change temperature
    @property
    def tempature(self):
        return self.__currentTemp
    
    @tempature.setter
    def tempature(self, newTemp):
        self.__currentTemp = newTemp
        
    #functions to modify humidity levels
    @property
    def humidity(self):
        return self.__currentHumidity
    
    @humidity.setter
    def humidity(self, newHumidity):
        self.__currentHumidity = newHumidity
        
    #function to modify human activity
    @property
    def activity(self):
        return self.__currentActivity
    
    @activity.setter
    def activity(self, newActivity):
        self.__currentActivity = newActivity
        
    #function to modify CO level
    @property
    def carbonMonoxide(self):
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
    print("Current temperature: ", a.tempature)
    print("Current Humdiity: ", a.humidity, "%")
    print("Room Occupancy: ", a.activity)
    print("CO level: ", a.carbonMonoxide, "ppm")
    a.name = "Living Room"
    a.tempature  = 75
    a.humidity = 53
    a.activity = "Occupied"
    a.carbonMonoxide = 1.2
    print(a.name)
    print("Current temperature: ", a.tempature)
    print("Current Humdiity: ", a.humidity, "%")
    print("Room Occupancy: ", a.activity)
    print("CO level: ", a.carbonMonoxide, "ppm")
    
    print()


    
    
    
    