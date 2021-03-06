# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:37:22 2020

@author: Brandon Lasher
"""
from tkinter import *
from math import sqrt

class gui_hvac:
    def __init__(self):
        self.__hvac_obj = None       
        self.hvacCanvas = None

    #
    #Draws a trignale based on side or height referance
    # Used X offset / Y offset as center point!
    def drawDownArrow(self, canvas, xOffset, yOffset, v, ref="h" ):
        
        if ref == "s":
            sideLen = v
            height = sideLen * sqrt(3) / 2
        else: #ref == "h":
            height = v
            sideLen = 2 * height / sqrt(3)
        
        p0 = (xOffset-sideLen/2, yOffset-height/2 )
        p1 = (xOffset, yOffset+height/2)
        p2 = (xOffset+sideLen/2, yOffset-height/2)
        
        return canvas.create_polygon( p0, p1, p2, fill="black")
    
    
    def drawUpArrow(self, canvas, xOffset, yOffset, v, ref="h"):
    
        if ref == "s":
            sideLen = v
            height = sideLen * sqrt(3) / 2
        else: #ref == "h":
            height = v
            sideLen = 2 * height / sqrt(3)    
    
        p0 = (xOffset-sideLen/2, yOffset + height/2)
        p1 = ( xOffset, yOffset - height/2)
        p2 = ( xOffset+sideLen/2, yOffset + height/2)
        return canvas.create_polygon( p0, p1, p2, fill="black")

    def drawHVAC( self, parent ):
        parent.update()
        ySize = parent.winfo_height();
        xSize = parent.winfo_width();
        
        
        yinc=int(ySize/5)
        self.xcol = [ 40, 40 + (xSize/2) - 5, 40 + (xSize/2) + 5]
        self.yRow = [ yinc, yinc*2, yinc*3, yinc*4 ] 
        
        self.hvacCanvas = Canvas(parent, width=xSize, height=ySize, bd=0, highlightthickness=0, bg="grey")
        self.hvacCanvas.pack()

        self.hvacCanvas.create_text(self.xcol[0], ySize/2, text="HVAC", font="Arial 24 bold underline", fill="black", anchor="s", angle=90)

        self.hvacCanvas.create_text( self.xcol[1], self.yRow[0], text ="Mode:", font="Arial 14 bold", fill="black", anchor="e", tags=("mode"))
        self.hvacCanvas.create_text( self.xcol[2], self.yRow[0], text ="" , font="Arial 14", fill="black", anchor="w", tags=("modeText"))

        self.hvacCanvas.create_text( self.xcol[1], self.yRow[1], text ="Fan:", font="Arial 14 bold", fill="black", anchor="e",  tags=("fan"))
        self.hvacCanvas.create_text(self.xcol[2], self.yRow[1], text ="" , font="Arial 14", fill="black", anchor="w", tags=("fanText"))

        self.hvacCanvas.create_text( self.xcol[1], self.yRow[2], text ="Exterior Temp:", font="Arial 14 bold", anchor="e", fill="black", tags=("extTemp"))
        self.hvacCanvas.create_text( self.xcol[2], self.yRow[2], text ="" , font="Arial 14", fill="black", anchor="w", tags=("extTempText"))
        
        upArrow = self.drawUpArrow( self.hvacCanvas, self.xcol[2]+75, self.yRow[2], yinc-10 )
        downArrow = self.drawDownArrow( self.hvacCanvas, self.xcol[2]+95, self.yRow[2], yinc-10 )
        
        
        #Changing the Temp here will auto update the Text via other
        # binding
        def incExtTemp():
            if self.hvac:
                self.hvac.exteriorTemp = self.hvac.exteriorTemp  + 1
            
        def decExtTemp():
            if self.hvac:
                self.hvac.exteriorTemp = self.hvac.exteriorTemp  - 1
        
        self.hvacCanvas.tag_bind( upArrow, "<Button-1>", lambda e:  incExtTemp() )
        self.hvacCanvas.tag_bind( downArrow, "<Button-1>", lambda e:  decExtTemp() )
        
        

        #self.hvacCanvas.create_text( self.xcol[1], self.yRow[3], text ="CFM:", font="Arial 14 bold", fill="black", anchor="e", tags=("cfm"))
        #self.hvacCanvas.create_text( self.xcol[2], self.yRow[3], text ="" , font="Arial 14", fill="black", anchor="w", tags=("cfmText"))
        
        #Set the initial Text
        self.updateAll()
        

    def updateMode(self):
        if( self.hvacCanvas and self.__hvac_obj ):
            self.hvacCanvas.itemconfigure( self.hvacCanvas.find_withtag('modeText'), text="{:<10}".format( str(self.hvac.modePretty()) ) ) 
            
    def updateCFM(self):
        if( self.hvacCanvas and self.__hvac_obj ):
            self.hvacCanvas.itemconfigure(self.hvacCanvas.find_withtag('cfmText'), text="{:<5}".format(str(self.hvac.cfm)))
            
    def updateExtTemp(self):
        if( self.hvacCanvas and self.__hvac_obj ):
            self.hvacCanvas.itemconfigure( self.hvacCanvas.find_withtag('extTempText'), text=u"{:>3}\N{DEGREE SIGN} F".format(str(self.hvac.exteriorTemp)))
            
    def updateFanMode(self):
        if( self.hvacCanvas and self.__hvac_obj ):
            self.hvacCanvas.itemconfigure(self.hvacCanvas.find_withtag('fanText'), text="{:<5}".format( "Always On" if self.hvac.fanAlwaysOn else "On" if self.hvac.fanOn else "Off" ))
    
    def updateAll(self):
        self.updateMode()
        self.updateCFM()
        self.updateExtTemp()
        self.updateFanMode()

    @property
    def hvac(self):
        return self.__hvac_obj

    #When an HVAC is assigned to the GUI it 
    # will automatically add all the callbacks need for updating
    @hvac.setter
    def hvac(self, newHvac):
        self.__hvac_obj = newHvac
        self.__hvac_obj.bind_to_tag("mode", self.updateMode)
        self.__hvac_obj.bind_to_tag("fanOn", self.updateFanMode)
        self.__hvac_obj.bind_to_tag("fanAlwaysOn", self.updateFanMode)
        self.__hvac_obj.bind_to_tag("exteriorTemp",  self.updateExtTemp)
        #self.__hvac_obj.bind_to_tag("cfm", self.updateCFM)
    
    
if __name__ == "__main__":
    
    
    import iglu_hvac
    import time
    
    def update(obj):
        obj.hvac_obj.mode = "Off"
        obj.updateMode()
    
    mainWindow = Tk()
    xVal = 600;
    yVal = 125;
    mainWindow.geometry(str(xVal)+"x"+str(yVal)) 
    gui = gui_hvac()
    
    gui.hvac = iglu_hvac.iglu_hvac()
    
    
    gui.drawHVAC(mainWindow)
    

    mainloop()