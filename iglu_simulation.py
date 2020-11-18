# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:01:09 2020

@author: Brandon Lasher

"""

import iglu_hub
import iglu_hvac

import iglu_Timer
import gui_main

#
# Need to create GUI as a thread
# Need to set update funciton as timer


class iglu_simulation:
    def __init__(self):
        #make devices
        self.hub = iglu_hub.iglu_hub()
        self.hvac = iglu_hvac.iglu_hvac()
        
        #map funcs and vars to simulation level
        self.areaList = self.hub.areaList
        
        #bind Sim updates to global timer
        iglu_Timer.globalTimer.bind_to(self.updateSim)
        
        
        #define GUI and setup callback functions to update HUB
        self.gui = gui_main.gui_main()
        
        #Enviromental Callbacks
        self.gui.gui_env.addZoneCallback = self.hub.addArea    #Now when the area button is hit, it will also add an area here
        self.gui.gui_env.removeZoneCallback = self.hub.delArea #Now when the area button is hit, it will also remove an area here
        
        
        #Hub
        self.gui.gui_hub.hub = self.hub
        
        #SetHVAC
        self.hub.hvac = self.hvac
        self.gui.gui_hvac.hvac = self.hvac 
        self.gui.gui_hvac.updateAll()
        #bind update functions!
        
        #map add area button to simulation addArea
        
        
        self.gui.draw()
    
    
    #This is the main update function for the simulator
    # will run everytime a new clock occurs
    def updateSim(self, newTimeValue):
        #Change to calling hub update function?
        for a in self.areaList:
            # print( f"---------{newTimeValue}----------")
            # print( "T: " + str(a.tempature))
            # print( "H: " + str(a.humidity))
            # print( "A: " + str(a.activity))
            # print( "C: " + str(a.carbonMonoxide))
            for d in a.deviceList:
                if "updateSensors" in dir(d):
                    d.updateSensors()
                a.updateStats()
        if( newTimeValue % 10 == 0 ):
            if( self.hvac.mode == "Cooling"):
                self.hvac.startHeating()
            else:
                self.hvac.startCooling()
                
        if( newTimeValue % 15 == 0 ):
            if( self.hvac.fanAlwaysOn ):
                self.hvac.fanAlwaysOn = False
            else:
                self.hvac.fanAlwaysOn = True
                
                

        
        
    def start(self):
        self.gui.startUI()    


if __name__ == "__main__":
    sim =  iglu_simulation()
    sim.start()
    
