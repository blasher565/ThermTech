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
        
        #Hub
        self.gui.gui_hub.hub = self.hub
        
        #SetHVAC
        self.hub.hvac = self.hvac
        self.gui.gui_hvac.hvac = self.hvac 
        self.gui.gui_hvac.updateAll()
        
        self.gui.gui_env.hub = self.hub
        #bind update functions!
        
        #map add area button to simulation addArea
        
        
        self.gui.draw()
    
    
    #This is the main update function for the simulator
    # will run everytime a new clock occurs
    def updateSim(self, newTimeValue):

        #
        for a in self.areaList:
            #Update HVAC mode for actual temp changes
            # If hotter outside: "+1", if colder outside: "-1"
            a.extRateSign =   1 if self.hvac.exteriorTemp > a.currentTempatureActual else ( -1 if  self.hvac.exteriorTemp < a.currentTempatureActual else 0 )
            a.hvacMode = self.hvac.mode # If heating: "+1", if cooling outside: "-1", if standby: 0
            
            #Update the Actual room temps
            a.updateCurrentTemp()

        
    def start(self):
        self.gui.startUI()    


if __name__ == "__main__":
    sim =  iglu_simulation()
    sim.start()
    
