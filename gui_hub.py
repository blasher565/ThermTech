# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 17:31:24 2020

@author: Brandon Lasher
"""
from tkinter import *
from PIL import Image, ImageTk

from  math import *
from iglu_Timer import *
from iglu_utils import *
import calendar

class gui_hub:
    def __init__(self):
        #will be used to store callback functions
        self.__hub = None
        self.hubCanvas = None
        self.timeCanvas = None
        self.xSize = 0;
        self.ySize = 0;
        
        self.currentScreen = "main"
        


    
    @property
    def hub(self):
        return self.__hub
    
    @hub.setter
    def hub(self, newHub):
        self.__hub = newHub
        self.hub.bind_to_tag( ("hub_gui", "addArea") , lambda: self.refreshScreen(self.currentScreen) )
        self.hub.bind_to_tag( ("hub_gui", "delArea") , lambda: self.refreshScreen(self.currentScreen) )
        

    def drawHub(self, parent ):
        parent.update()
        self.ySize = parent.winfo_height();
        self.xSize = parent.winfo_width();
        

        #print( xSize, ySize)
        displayFrame_height = self.ySize;
        
        #create frame
        displayFrame = Frame( parent, width=self.xSize, height=displayFrame_height)
        displayFrame.grid(row=0, column=0, sticky=N+E+S+W)
        
        #globals needed for images
        global  wifiImg, sideButtonBg, sideButtonBgHover, windowBg, upButton, downButton, areaButtonBg, areaButtonBgHover
        
        wifiImg = ImageTk.PhotoImage(file = r"./images/wifi.png") 
        windowBg = resizeImage(r"./images/screenBg.png", self.xSize, self.ySize)   #set the main canvas BG
        
        sideButtonBg = resizeImage(r"./images/buttonBg.png", 150, 75 )   #set the button canvas BG
        sideButtonBgHover = resizeImage(r"./images/buttonBgHover.png", 150, 75 )   #set the button canvas BG
        
        areaButtonBg = resizeImage(r"./images/buttonBg.png", 250, 75 )   #set the button canvas BG
        areaButtonBgHover = resizeImage(r"./images/buttonBgHover.png", 250, 75 )   #set the button canvas BG
        
        upButton = resizeImage(r"./images/upButton.png", 75, 75)
        downButton = resizeImage(r"./images/downButton.png", 75, 75)
        
        #
        # Top display bar
        #
       
        
        self.timeCanvas = Canvas(parent, width=self.xSize, height=30, bd=0, highlightthickness=0, bg="#000000000")
        self.timeCanvas.grid(row=0, column=0, sticky=N)
        timeText = self.timeCanvas.create_text(self.xSize/2, 15, text="{:%I:%M %p}".format(globalTimer.absTime), font=("Arial 12 bold"), fill="white" )
        globalTimer.bind_to( lambda t: self.timeCanvas.itemconfigure(timeText, text="{:%I:%M %p}".format(globalTimer.absTime) ) )
        
        dateText = self.timeCanvas.create_text(85, 15, text="{:%a, %b %d, %Y}".format(globalTimer.absTime), font=("Arial 12 bold"), fill="white" )
        globalTimer.bind_to( lambda t: self.timeCanvas.itemconfigure(dateText, text="{:%a, %b %d, %Y}".format(globalTimer.absTime) ) )
         
        
        
        connectionImage = self.timeCanvas.create_image(self.xSize-30, 15, image=wifiImg )
        #bind to connection manager and update the immage accordingly
    
        #Define menu Items!
        self.hubCanvas = Canvas(displayFrame, width=self.xSize, height=self.ySize, bd=0, highlightthickness=0, bg="orange")
        self.hubCanvas.pack(fill=BOTH)
        self.hubCanvas.create_image(self.xSize/2, self.ySize/2, image=windowBg )
        
        buttonOffset = 125
        buttonSpacing = 15
        homeFunc = lambda e:   self.refreshScreen("main")
        self.makeMenuButton( self.hubCanvas, (self.xSize-sideButtonBg.width()/2), buttonOffset, "Home", command=homeFunc )
    
    
        areaFunc = lambda e:  self.refreshScreen("areas")
        self.makeMenuButton( self.hubCanvas, (self.xSize-sideButtonBg.width()/2), buttonOffset+sideButtonBg.height()+buttonSpacing, "Areas",  command=areaFunc)
        
    
        settingFunc = lambda e: self.refreshScreen("settings")
        self.makeMenuButton( self.hubCanvas, (self.xSize-sideButtonBg.width()/2), buttonOffset+(sideButtonBg.height()+buttonSpacing)*2, "Settings", command=settingFunc )
    
        homeFunc(None)
    
        
        displayFrame.update()
        
    def refreshScreen(self, screenName ):
        if( screenName == "main"):
            self.drawHomeScreen(self.hubCanvas, self.xSize, self.ySize )
        elif( screenName == "areas"):
            self.drawAreaScreen(self.hubCanvas, self.xSize, self.ySize )
        elif( screenName == "settings"):
            self.drawSettingsScreen(self.hubCanvas, self.xSize, self.ySize )
        else:
            pass
        
        
        
    
    def clearScreenWithTag(self, canvas, tagID ):
        for i in canvas.find_withtag(tagID):
            canvas.delete(i)
            
    
    def clearAllScreen(self, canvas ):
        self.clearScreenWithTag(canvas, "mainWindow")
        self.clearScreenWithTag(canvas, "areasWindow")
        self.clearScreenWithTag(canvas, "settingsWindow")
    
    
    
    def makeMenuButton(self, canvasLoc, *args, **kwargs ):
        if "tags" in kwargs:
            buttonCanvas = canvasLoc.create_image(args[0], args[1],image=sideButtonBg, tags=kwargs["tags"])
            textCanvas =  canvasLoc.create_text(args[0], args[1], text=args[2], font=("Arial 15 bold"), fill="#ffffff", tags=kwargs["tags"] )
        else:
            buttonCanvas = canvasLoc.create_image(args[0], args[1],image=sideButtonBg)
            textCanvas =  canvasLoc.create_text(args[0], args[1], text=args[2], font=("Arial 15 bold"), fill="#ffffff" )
        
        #Need to add to both due 
        canvasLoc.tag_bind( buttonCanvas, "<Enter>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=sideButtonBgHover  ) )
        canvasLoc.tag_bind( buttonCanvas, "<Leave>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=sideButtonBg  ) )
        canvasLoc.tag_bind( textCanvas, "<Enter>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=sideButtonBgHover  ) )
        canvasLoc.tag_bind( textCanvas, "<Leave>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=sideButtonBg  ) )
        
        #mouse down command
        if "command" in kwargs:
            canvasLoc.tag_bind( buttonCanvas, "<Button-1>", kwargs["command"])
            canvasLoc.tag_bind( textCanvas, "<Button-1>", kwargs["command"]) 
        
        return buttonCanvas, textCanvas
    
    def makeAreaButton(self, canvasLoc, *args, **kwargs ):
        if "tags" in kwargs:
            buttonCanvas = canvasLoc.create_image(args[0], args[1],image=areaButtonBg, tags=kwargs["tags"])
            textCanvas =  canvasLoc.create_text(args[0], args[1], text=args[2], font=("Arial 15 bold"), fill="#ffffff", tags=kwargs["tags"] )
        else:
            buttonCanvas = canvasLoc.create_image(args[0], args[1],image=areaButtonBg)
            textCanvas =  canvasLoc.create_text(args[0], args[1], text=args[2], font=("Arial 15 bold"), fill="#ffffff" )
        
        #Need to add to both due 
        canvasLoc.tag_bind( buttonCanvas, "<Enter>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=areaButtonBgHover  ) )
        canvasLoc.tag_bind( buttonCanvas, "<Leave>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=areaButtonBg  ) )
        canvasLoc.tag_bind( textCanvas, "<Enter>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=areaButtonBgHover  ) )
        canvasLoc.tag_bind( textCanvas, "<Leave>", lambda e: canvasLoc.itemconfigure(buttonCanvas, image=areaButtonBg  ) )
        
        #mouse down command
        if "command" in kwargs:
            canvasLoc.tag_bind( buttonCanvas, "<Button-1>", kwargs["command"])
            canvasLoc.tag_bind( textCanvas, "<Button-1>", kwargs["command"]) 
        
        return buttonCanvas, textCanvas
    
    #
    #
    #
    #
    #
    def drawHomeScreen(self, canvas, screenSizex, screenSizey ):
        
        #clear out other screens
        self.clearAllScreen( canvas )
        if( self.hub ):
            self.hub.delete_bind_tag( "hub_gui" ) #any bind here will have the tag for the element at that it is coming from the gui This allows for screen clears
        self.currentScreen = "main"
        
        xNameOffset = 30
        yNameOffset = 40
        
        getName = lambda: self.hub and (self.hub.getPrimaryArea().name if self.hub.getPrimaryArea() else "Area Name" )
        areaName = canvas.create_text(xNameOffset, yNameOffset, text=getName() , font="Arial 30", fill="white", anchor="nw", tags=('mainWindow', 'area1Name') )
        bounds = canvas.bbox(areaName)  # returns a tuple like (x1, y1, x2, y2)
        
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        # canvas.coords(areaName, bounds[2], bounds[3]+yNameOffset )
        # canvas.coords(areaName, bounds[2], bounds[3]+yNameOffset )
        
        #(x1, y1, x2, y2)
        canvas.create_line(0, height+yNameOffset, width+100+xNameOffset ,  height+yNameOffset , fill="white", width=3 , tags=('mainWindow') )
        canvas.create_line(0, height+yNameOffset+5, width+75+xNameOffset ,  height+yNameOffset+5 , fill="white", width=1 , tags=('mainWindow') )    
        
        # if primary area is set or primary area has name changed
        if( self.hub ):
            self.hub.bind_to_tag( ("hub_gui", "primaryArea") , lambda: canvas.itemconfigure(areaName, text=getName() ))
            if( self.hub.getPrimaryArea() ):
                self.hub.getPrimaryArea().bind_to_tag( ("hub_gui", "name" ), lambda: canvas.itemconfigure(areaName, text=getName() ) )
            
    
        #Draw Target temp    
        ytextLoc = 275
        xtextLoc = 340
        pad = 0
        getTargetTemp = lambda: "{:02.0f}\N{DEGREE SIGN}".format(self.hub.getPrimaryArea().targetTempature if self.hub.getPrimaryArea() else 0 );
        targetTempText = canvas.create_text(xtextLoc, ytextLoc, text=getTargetTemp() , font="Arial 90 ", fill="white", tags=('mainWindow','targetTemp') )
        
        self.hub.bind_to_tag( ("hub_gui", "primaryArea") , lambda: canvas.itemconfigure(targetTempText, text=getTargetTemp() ))
        if( self.hub.getPrimaryArea() ):
            self.hub.getPrimaryArea().bind_to_tag( ("hub_gui", "targetTempature" ), lambda: canvas.itemconfigure(targetTempText, text=getTargetTemp() ) )
            
        
        bounds = canvas.bbox(targetTempText)  # returns a tuple like (x1, y1, x2, y2)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        upButtonRef = canvas.create_image(xtextLoc-20, int(bounds[1] - upButton.height()/2 - pad ) , image = upButton, tags=('mainWindow'))
        downButtonRef = canvas.create_image(xtextLoc-20, int(bounds[3] + upButton.height()/2 + pad ) , image = downButton, tags=('mainWindow'))
        
        def decTargetTemp():
            if( self.hub.getPrimaryArea() ):
                self.hub.getPrimaryArea().targetTempature = self.hub.getPrimaryArea().targetTempature - 1
            
        def incTargetTemp():
            if( self.hub.getPrimaryArea() ):
                self.hub.getPrimaryArea().targetTempature = self.hub.getPrimaryArea().targetTempature + 1
            
        canvas.tag_bind( upButtonRef, "<Button-1>", lambda e:  incTargetTemp() )
        canvas.tag_bind( downButtonRef, "<Button-1>", lambda e:  decTargetTemp() ) 
        
    
        #Draw Current temp  
        ytextLoc = 135
        xtextLoc = 110
        insideLabel = canvas.create_text(xtextLoc, ytextLoc, text=u'Inside', font="Arial 20 underline", fill="white", anchor='n', tags=('mainWindow') )
 
        bounds2 = canvas.bbox(insideLabel) 
        width = bounds2[2] - bounds2[0]
        height = bounds2[3] - bounds2[1]
        
                
        getInsideTemp = lambda: u"Temp: {:>02.0f}\N{DEGREE SIGN}".format( self.hub.getPrimaryArea().currentTempature if self.hub.getPrimaryArea() else 0 );
        currentTempText = canvas.create_text(xtextLoc, bounds2[3]+10, text=getInsideTemp(), font="Arial 20 ", fill="white", anchor='n', tags=('mainWindow', 'area1Temp') )
        
        self.hub.bind_to_tag( ("hub_gui", "primaryArea") , lambda: canvas.itemconfigure(currentTempText, text=getCurrentTemp() ))
        if( self.hub.getPrimaryArea() ):
            self.hub.getPrimaryArea().bind_to_tag( ("hub_gui", "currentTempature" ), lambda: canvas.itemconfigure(currentTempText, text=getInsideTemp() ) )
            
        bounds = canvas.bbox(currentTempText) 
        
        getCurrentHumidity = lambda: u"Humidity:{:>3.0f}%".format( self.hub.getPrimaryArea().currentHumidity if self.hub.getPrimaryArea() else 0 );
        humText = canvas.create_text(xtextLoc, bounds[3]+10, text=getCurrentHumidity(), font="Arial 20", fill="white", anchor="n", tags=('mainWindow', 'area1Humidity') )
       
        self.hub.bind_to_tag( ("hub_gui", "primaryArea") , lambda: canvas.itemconfigure(humText, text=getCurrentHumidity() ))
        if( self.hub.getPrimaryArea() ):
            self.hub.getPrimaryArea().bind_to_tag( ("hub_gui", "currentHumidity" ), lambda: canvas.itemconfigure(humText, text=getCurrentHumidity() ) )
            
        bounds2 = canvas.bbox(humText) 
            
        outsideLabel = canvas.create_text(xtextLoc, bounds2[3]+35, text=u'Outside', font="Arial 20 underline", fill="white", anchor='n', tags=('mainWindow') )
        bounds2 = canvas.bbox(outsideLabel) 
        getOutsideTemp = lambda: u"Temp: {:>02.0f}\N{DEGREE SIGN}".format( self.hub.hvac.exteriorTemp if self.hub.hvac else 0 );
        outsideTempText = canvas.create_text(xtextLoc, bounds2[3]+10, text=getOutsideTemp(), font="Arial 20 ", fill="white", anchor='n', tags=('mainWindow', 'area1Temp') )
        if( self.hub.hvac ):
            self.hub.hvac.bind_to_tag( ("hub_gui", "exteriorTemp" ), lambda: canvas.itemconfigure(outsideTempText, text=getOutsideTemp() ) )
        
        #Bottom summary
        yLineLoc = screenSizey - 110
        canvas.create_line( int(screenSizex*.05) , yLineLoc, int(screenSizex*.95) , yLineLoc , fill="white", width=1 , tags=('mainWindow') )
        
        ySummary = yLineLoc-20
        xSummary = int(screenSizex*.1)
        summaryText = canvas.create_text(xSummary, ySummary, text=u'Status', font="Arial 25", fill="white", anchor="w", tags=('mainWindow') )    
        
        
        getHVACMode = lambda: u"{}".format( self.hub.hvac.modePretty() if self.hub.hvac else "Standby")
        modeText = canvas.create_text(xSummary, ySummary+45, text=getHVACMode(), font="Arial 25", fill="white", anchor="w", tags=('mainWindow', 'HVACMode') )
        if( self.hub.hvac ):
            self.hub.hvac.bind_to_tag( ("hub_gui", "mode" ), lambda: canvas.itemconfigure(modeText, text=getHVACMode() ) )
        

        getHVACFan = lambda: u"Fan: {:<5}".format( ("Always On" if self.hub.hvac.fanAlwaysOn else "On" if self.hub.hvac.fanOn else "Off") if self.hub.hvac else "Off" )
        fanText = canvas.create_text(xSummary, ySummary+90, text=getHVACFan(), font="Arial 25", fill="white", anchor="w", tags=('mainWindow', 'HVACMode') )
        if( self.hub.hvac ):
            self.hub.hvac.bind_to_tag( ("hub_gui", "fanOn" ), lambda: canvas.itemconfigure(fanText, text=getHVACFan() ) )
            self.hub.hvac.bind_to_tag( ("hub_gui", "fanAlwaysOn" ), lambda: canvas.itemconfigure(fanText, text=getHVACFan() ) )
    
        #if area 2 or 3 
        getArea2Name = lambda: (self.hub.getSecondaryArea().name if self.hub.getSecondaryArea() else "" )
        getArea2Temp = lambda: "{:}".format( u"{:>02.0f}\N{DEGREE SIGN}".format( self.hub.getSecondaryArea().currentTempature) if self.hub.getSecondaryArea() else "" )
        getArea2Hum = lambda: "{:}".format( u"{:>3.0f}%".format( self.hub.getSecondaryArea().currentHumidity) if self.hub.getSecondaryArea() else "" )
        
        areas2Name = canvas.create_text(int(screenSizex*.60), ySummary, text=getArea2Name(), font="Arial 25", fill="white", tags=('mainWindow', 'area2Name') )
        area2Temp = canvas.create_text(int(screenSizex*.60), ySummary+45, text=getArea2Temp(), font="Arial 25", fill="white", tags=('mainWindow', 'area2Temp') )
        area2Humd = canvas.create_text(int(screenSizex*.60), ySummary+90, text=getArea2Hum(), font="Arial 25", fill="white", tags=('mainWindow', 'area2Humidity') )
        
        self.hub.bind_to_tag( ("hub_gui", "secondaryArea") , lambda: canvas.itemconfigure(areas2Name, text=getArea2Name() ))
        self.hub.bind_to_tag( ("hub_gui", "secondaryArea") , lambda: canvas.itemconfigure(area2Temp, text=getArea2Temp() ))
        self.hub.bind_to_tag( ("hub_gui", "secondaryArea") , lambda: canvas.itemconfigure(area2Humd, text=getArea2Hum() ))
        if( self.hub.getSecondaryArea() ):
            self.hub.getSecondaryArea().bind_to_tag( ("hub_gui", "name" ), lambda: canvas.itemconfigure(areas2Name, text=getArea2Name() ) )
            self.hub.getSecondaryArea().bind_to_tag( ("hub_gui", "currentTempature" ), lambda: canvas.itemconfigure(area2Temp, text=getArea2Temp() ) )
            self.hub.getSecondaryArea().bind_to_tag( ("hub_gui", "currentHumidity" ), lambda: canvas.itemconfigure(area2Humd, text=getArea2Hum() ) )
        
        
        getArea3Name = lambda: (self.hub.getTertiaryArea().name if self.hub.getTertiaryArea() else "" )
        getArea3Temp = lambda: "{:}".format( u"{:>02.0f}\N{DEGREE SIGN}".format( self.hub.getTertiaryArea().currentTempature) if self.hub.getTertiaryArea() else "" )
        getArea3Hum = lambda: "{:}".format( u"{:>3.0f}%".format( self.hub.getTertiaryArea().currentHumidity) if self.hub.getTertiaryArea() else "" )
        
        
        area3Name = canvas.create_text(int(screenSizex*.80), ySummary, text=getArea3Name(), font="Arial 25", fill="white", tags=('mainWindow', 'area3Name') )
        area3Temp = canvas.create_text(int(screenSizex*.80), ySummary+45, text=getArea3Temp(), font="Arial 25", fill="white", tags=('mainWindow', 'area3Temp') )
        area3Humd = canvas.create_text(int(screenSizex*.80), ySummary+90, text=getArea3Hum(), font="Arial 25", fill="white", tags=('mainWindow', 'area3Humidity') )
    
        self.hub.bind_to_tag( ("hub_gui", "tertiaryArea") , lambda: canvas.itemconfigure(area3Name, text=getArea3Name() ))
        self.hub.bind_to_tag( ("hub_gui", "tertiaryArea") , lambda: canvas.itemconfigure(area3Temp, text=getArea3Temp() ))
        self.hub.bind_to_tag( ("hub_gui", "tertiaryArea") , lambda: canvas.itemconfigure(area3Humd, text=getArea3Hum() ))
        if( self.hub.getTertiaryArea() ):
            self.hub.getTertiaryArea().bind_to_tag( ("hub_gui", "name" ), lambda: canvas.itemconfigure(area3Name, text=getArea3Name() ) )
            self.hub.getTertiaryArea().bind_to_tag( ("hub_gui", "currentTempature" ), lambda: canvas.itemconfigure(area3Temp, text=getArea3Temp() ) )
            self.hub.getTertiaryArea().bind_to_tag( ("hub_gui", "currentHumidity" ), lambda: canvas.itemconfigure(area3Humd, text=getArea3Hum() ) )
        
    
        self.bindHomeScreen( canvas )
        
    
    #Go through an bind each element for change
    def bindHomeScreen(self, canvas ):
    
        #
        # NEED TO BIND for updates
        #    
        # canvas.find_withtag('targetTemp')
        # canvas.find_withtag('area1Name')
        # canvas.find_withtag('area1Temp')
        # canvas.find_withtag('area1Humidity')    
        # canvas.find_withtag('area2Name')
        # canvas.find_withtag('area2Temp')
        # canvas.find_withtag('area2Humidity')
        # canvas.find_withtag('area3Name')
        # canvas.find_withtag('area3Temp')
        # canvas.find_withtag('area3Humidity')
        # canvas.find_withtag('HVACMode')
        
        pass
        
    
    def drawAreaScreen(self, canvas, screenSizex, screenSizey ):
        self.clearAllScreen( canvas )
        self.hub.delete_bind_tag( "hub_gui" ) 
        self.currentScreen = "areas"
        
        xNameOffset = 30
        yNameOffset = 40
        areaName = canvas.create_text(xNameOffset, 0, text=u'Area Settings', font="Arial 30", fill="white", tags=('mainWindow', 'area1Name') )
        bounds = canvas.bbox(areaName)  # returns a tuple like (x1, y1, x2, y2)
        
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        canvas.coords(areaName, bounds[2], bounds[3]+yNameOffset )
        
        #(x1, y1, x2, y2)
        canvas.create_line(0, height+yNameOffset, width+100+xNameOffset ,  height+yNameOffset , fill="white", width=3 , tags=('mainWindow') )
        canvas.create_line(0, height+yNameOffset+5, width+75+xNameOffset ,  height+yNameOffset+5 , fill="white", width=1 , tags=('mainWindow') )
        
        areaDetailFunc= lambda e: self.drawAreaDetailScreen(canvas, screenSizex, screenSizey, 0)
        self.makeAreaButton( canvas, (screenSizex*.37), (screenSizey*.25), "Area Name", tags=('areasWindow'), command=areaDetailFunc)
        
        
        
    def drawAreaDetailScreen(self, canvas, screenSizex, screenSizey, areaID ):
        self.clearAllScreen( canvas )
        self.hub.delete_bind_tag( "hub_gui" ) 
        self.currentScreen = "settings"
        
        xNameOffset = 30
        yNameOffset = 40
        areaName = canvas.create_text(xNameOffset, 0, text=u'Area Name', font="Arial 30", fill="white", tags=('mainWindow', 'area1Name') )
        bounds = canvas.bbox(areaName)  # returns a tuple like (x1, y1, x2, y2)
        
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        canvas.coords(areaName, bounds[2], bounds[3]+yNameOffset )
        
        #(x1, y1, x2, y2)
        canvas.create_line(0, height+yNameOffset, width+100+xNameOffset ,  height+yNameOffset , fill="white", width=3 , tags=('mainWindow') )
        canvas.create_line(0, height+yNameOffset+5, width+75+xNameOffset ,  height+yNameOffset+5 , fill="white", width=1 , tags=('mainWindow') )   
        
        #Rename Area?
        #Set primary, secondary, None
        #Device List? 
        
    
    def drawSettingsScreen( self, canvas, screenSizex, screenSizey ):
        self.clearAllScreen( canvas )


if __name__ == "__main__":
    mainWindow = Tk()
    import iglu_hub
    xVal = 600;
    yVal = 623;
    mainWindow.geometry(str(xVal)+"x"+str(yVal)) 
    mainWindow.update()
    gui = gui_hub()
    gui.hub = iglu_hub.iglu_hub()
    gui.drawHub(mainWindow)
    mainloop()