# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:01:44 2020

@author: Brandon Lasher

Simple HVAC class which holds the informaiton about the 
  HVAC systems
"""


class iglu_hvac:
    def __init__(self, mode = "Standby", cfm = 2000, exteriorTemp = 70, fanAlwaysOn=False ):

        self.__mode = mode
        self.__cfm = cfm;  # cubic feet per minute
        self.__exteriorTemp = exteriorTemp
        
        self.__fanAlwaysOn = fanAlwaysOn;
        self.__fanOn = fanAlwaysOn;
        if not fanAlwaysOn:
            self.__fanOn = (mode == "Cooling") or (mode == "Heating");
            
            
    #print function
    def __repr__(self):
        out = "HVAC Info\n------------------\n"
        out += "Exterior Temp: {:}\n".format(self.exteriorTemp)
        out += "Mode: {:}\n".format(self.mode)
        out += "Fan: {:}, AlwaysOn: {:}\n".format(self.__fanOn, self.__fanAlwaysOn )
        out += "CFM: {:}\n".format(self.cfm)
        return out

    @property
    def mode( self ):
        return self.__mode
    
    @mode.setter
    def mode( self, newMode ):
        self.__mode = newMode
        
    @property
    def cfm( self ):
        return self.__cfm
    
    @cfm.setter
    def cfm( self, newCfm ):
        self.__cfm = newCfm

    @property
    def exteriorTemp( self ):
        return self.__exteriorTemp
    
    @exteriorTemp.setter
    def exteriorTemp( self, newTemp ):
        self.__exteriorTemp = newTemp
        
    @property
    def fanAlwaysOn( self ):
        return self.__fanAlwaysOn
    
    @fanAlwaysOn.setter
    def exteriorTemp( self, newAlwaysOn ):
        self.__fanAlwaysOn = newAlwaysOn    
        self.__fanOn = newAlwaysOn  
        
        
    def startCooling( self ):
        self.mode = "Cooling"
        self.__fanOn = True;
        
    def startHeating( self ):
        self.mode = "Heating"
        self.__fanOn = True;
        
    def stop(self):
        self.mode = "Standby"
        if not( self.fanAlwaysOn ):
            self.__fanOn = False
        
if __name__ == "__main__":
    hvac = iglu_hvac()
    print( hvac )
    