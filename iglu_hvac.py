# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:01:44 2020

@author: Brandon Lasher

Simple HVAC class which holds the informaiton about the 
  HVAC systems
"""


class iglu_hvac:
    def __init__(self, mode = 0, cfm = 2000, exteriorTemp = 70, fanAlwaysOn=False ):

        self.__mode = mode
        self.__cfm = cfm;  # cubic feet per minute
        self.__exteriorTemp = exteriorTemp
        
        self.__fanAlwaysOn = fanAlwaysOn;
        self.__fanOn = fanAlwaysOn;
        if not fanAlwaysOn:
            self.__fanOn = (mode == 1) or (mode == -1);
            
        self.__observers = []
            
            
    #print function
    def __repr__(self):
        out = "HVAC Info\n------------------\n"
        out += "Exterior Temp: {:}\n".format(self.exteriorTemp)
        out += "Mode: {:}\n".format(self.mode)
        out += "Fan: {:}, AlwaysOn: {:}\n".format(self.__fanOn, self.__fanAlwaysOn )
        out += "CFM: {:}\n".format(self.cfm)
        return out

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

    @property
    def mode( self ):
        return self.__mode
    
    @mode.setter
    def mode( self, newMode ):
        self.__mode = newMode
        self.runCallback( "mode")
        
  
    def modePretty( self ):
        return  "Standby" if self.__mode == 0 else ( "Cooling"  if self.__mode == -1 else "Heating")        
        
    @property
    def cfm( self ):
        return self.__cfm
    
    @cfm.setter
    def cfm( self, newCfm ):
        self.__cfm = newCfm
        self.runCallback( "cfm")

    @property
    def exteriorTemp( self ):
        return self.__exteriorTemp
    
    @exteriorTemp.setter
    def exteriorTemp( self, newTemp ):
        self.__exteriorTemp = newTemp
        self.runCallback( "exteriorTemp")
        
    @property
    def fanAlwaysOn( self ):
        return self.__fanAlwaysOn
    
    @fanAlwaysOn.setter
    def fanAlwaysOn( self, newAlwaysOn ):
        self.__fanAlwaysOn = newAlwaysOn    
        self.runCallback( "fanAlwaysOn")
        
        #Update the current Fan to be On
        if not( self.mode == -1 or self.mode == 1):
            self.fanOn = newAlwaysOn
        
                
    @property
    def fanOn( self ):
        return self.__fanOn   
    
    @fanOn.setter
    def fanOn( self, fanVal ):
        self.__fanOn = fanVal
        self.runCallback( "fanOn")
        
        
    def startCooling( self ):
        self.mode = -1
        self.fanOn = True;
        
    def startHeating( self ):
        self.mode = 1
        self.fanOn = True;
        
    def stop(self):
        self.mode = 0
        if not( self.fanAlwaysOn ):
            self.__fanOn = False
        
if __name__ == "__main__":
    
    import time
    def printWords( inputStr ):
        print(inputStr)
    
    hvac = iglu_hvac()
    print( hvac )
    
    time.sleep(2)
    
    hvac.bind_to_tag(("mode"), lambda: printWords("MODE CHANGE"))
    hvac.bind_to_tag("fanOn", lambda: printWords("FAN CHANGE"))
    hvac.bind_to_tag("exteriorTemp", lambda: printWords("EXT CHANGE"))
    hvac.bind_to_tag("cfm", lambda: printWords("CFM CHANGE"))
    
    hvac.startCooling()
    
    
    
    
    
    