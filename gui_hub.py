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

def drawHub( parent ):
    parent.update()
    ySize = parent.winfo_height();
    xSize = parent.winfo_width();

    displayFrame_height = ySize;
    
    #create frame
    displayFrame = Frame( parent, width=xSize, height=displayFrame_height)
    displayFrame.grid(row=0, column=0, sticky=N)
    
    #globals needed for images
    global  wifiImg, sideButtonBg, sideButtonBgHover, windowBg, upButton, downButton, areaButtonBg, areaButtonBgHover
    
    wifiImg = ImageTk.PhotoImage(file = r"./images/wifi.png") 
    windowBg = resizeImage(r"./images/screenBg.png", xSize, ySize)   #set the main canvas BG
    
    sideButtonBg = resizeImage(r"./images/buttonBg.png", 200, 75 )   #set the button canvas BG
    sideButtonBgHover = resizeImage(r"./images/buttonBgHover.png", 200, 75 )   #set the button canvas BG
    
    areaButtonBg = resizeImage(r"./images/buttonBg.png", 400, 75 )   #set the button canvas BG
    areaButtonBgHover = resizeImage(r"./images/buttonBgHover.png", 400, 75 )   #set the button canvas BG
    
    upButton = resizeImage(r"./images/upButton.png", 100, 100)
    downButton = resizeImage(r"./images/downButton.png", 100, 100)
    
    #
    # Top display bar
    #
    persistantItems = {}
    mainSreenItems = {}
    
    
    persistantItems["timeCanvas"] = Canvas(parent, width=xSize, height=30, bd=0, highlightthickness=0, bg="#000000000")
    persistantItems["timeCanvas"].grid(row=0, column=0, sticky=N)
    timeText = persistantItems["timeCanvas"].create_text(xSize/2, 15, text="{:%I:%M %p}".format(globalTimer.absTime), font=("Arial 12 bold"), fill="white" )
    globalTimer.bind_to( lambda t: persistantItems["timeCanvas"].itemconfigure(timeText, text="{:%I:%M %p}".format(globalTimer.absTime) ) )
    
    dateText = persistantItems["timeCanvas"].create_text(85, 15, text="{:%a, %b %d, %Y}".format(globalTimer.absTime), font=("Arial 12 bold"), fill="white" )
    globalTimer.bind_to( lambda t: persistantItems["timeCanvas"].itemconfigure(dateText, text="{:%a, %b %d, %Y}".format(globalTimer.absTime) ) )
     
    
    
    connectionImage = persistantItems["timeCanvas"].create_image(xSize-30, 15, image=wifiImg )
    #bind to connection manager and update the immage accordingly

    #Define menu Items!
    persistantItems["mainCanvas"] = Canvas(displayFrame, width=xSize, height=ySize, bd=0, highlightthickness=0, bg="orange")
    persistantItems["mainCanvas"].pack(fill=BOTH)
    persistantItems["mainCanvas.bg"] = persistantItems["mainCanvas"].create_image(xSize/2, ySize/2, image=windowBg )
    
    buttonOffset = 125
    buttonSpacing = 15
    homeFunc = lambda e:   drawHomeScreen(persistantItems["mainCanvas"], xSize, ySize )
    persistantItems["mainCanvas.HomeBut"], persistantItems["mainCanvas.HomeText"] = makeMenuButton( persistantItems["mainCanvas"], (xSize-sideButtonBg.width()/2), buttonOffset, "Home", command=homeFunc )


    areaFunc = lambda e:  drawAreaScreen(persistantItems["mainCanvas"], xSize, ySize )
    persistantItems["mainCanvas.AreaBut"], persistantItems["mainCanvas.AreaText"] = makeMenuButton( persistantItems["mainCanvas"], (xSize-sideButtonBg.width()/2), buttonOffset+sideButtonBg.height()+buttonSpacing, "Areas",  command=areaFunc)
    

    settingFunc = lambda e: drawSettingsScreen(persistantItems["mainCanvas"], xSize, ySize )
    persistantItems["mainCanvas.SettingsBut"], persistantItems["mainCanvas.SettingsText"] = makeMenuButton( persistantItems["mainCanvas"], (xSize-sideButtonBg.width()/2), buttonOffset+(sideButtonBg.height()+buttonSpacing)*2, "Settings", command=settingFunc )

    homeFunc(None)

    
    displayFrame.update()

def clearScreenWithTag( canvas, tagID ):
    for i in canvas.find_withtag(tagID):
        canvas.delete(i)
        

def clearAllScreen( canvas ):
    clearScreenWithTag(canvas, "mainWindow")
    clearScreenWithTag(canvas, "areasWindow")
    clearScreenWithTag(canvas, "settingsWindow")



def makeMenuButton( canvasLoc, *args, **kwargs ):
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

def makeAreaButton( canvasLoc, *args, **kwargs ):
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

def drawHomeScreen( canvas, screenSizex, screenSizey ):
    
    #clear out other screens
    clearAllScreen( canvas )

    xNameOffset = 30
    yNameOffset = 40
    areaName = canvas.create_text(xNameOffset, 0, text=u'Area Name', font="Arial 36", fill="white", tags=('mainWindow', 'area1Name') )
    bounds = canvas.bbox(areaName)  # returns a tuple like (x1, y1, x2, y2)
    
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    canvas.coords(areaName, bounds[2], bounds[3]+yNameOffset )
    
    #(x1, y1, x2, y2)
    canvas.create_line(0, height+yNameOffset, width+100+xNameOffset ,  height+yNameOffset , fill="white", width=3 , tags=('mainWindow') )
    canvas.create_line(0, height+yNameOffset+5, width+75+xNameOffset ,  height+yNameOffset+5 , fill="white", width=1 , tags=('mainWindow') )


    #Draw Target temp    
    ytextLoc = 300
    xtextLoc = 410
    pad = -10
    targetTempText = canvas.create_text(xtextLoc, ytextLoc, text=u'00', font="Arial 135 ", fill="white", tags=('mainWindow','targetTemp') )
    #bind_to area with clock -- FIX
    
    bounds = canvas.bbox(targetTempText)  # returns a tuple like (x1, y1, x2, y2)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    canvas.create_text(bounds[2], bounds[1]+50, text=u'\N{DEGREE SIGN}', font="Arial 50", fill="white", tags=('mainWindow') )
    upButtonRef = canvas.create_image(xtextLoc, int(bounds[1] - upButton.height()/2 - pad ) , image = upButton, tags=('mainWindow'))
    downButtonRef = canvas.create_image(xtextLoc, int(bounds[3] + upButton.height()/2 + pad ) , image = downButton, tags=('mainWindow'))

    #Draw Current temp  
    currTempLabel = canvas.create_text(xtextLoc, ytextLoc, text=u'Current Temp:', font="Arial 25", fill="white", tags=('mainWindow') )
    bounds2 = canvas.bbox(currTempLabel) 
    width = bounds2[2] - bounds2[0]
    height = bounds2[3] - bounds2[1]
        
    xtextLoc = bounds[0] - width/2 - 50
    ytextLoc = bounds[1]
    
    canvas.coords(currTempLabel, xtextLoc, ytextLoc )
    
    bounds = canvas.bbox(currTempLabel)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    canvas.create_line(bounds[0], bounds[3], bounds[2], bounds[3], fill="white", width=1 , tags=('mainWindow') )
    
    targetTempText = canvas.create_text(xtextLoc, ytextLoc+height+20, text=u'00', font="Arial 40 ", fill="white", tags=('mainWindow', 'area1Temp') )
    #bind_to area with clock  -- FIX
    
    bounds = canvas.bbox(targetTempText)  # returns a tuple like (x1, y1, x2, y2)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    canvas.create_text(bounds[2]+5, bounds[1]+20, text=u'\N{DEGREE SIGN}', font="Arial 25", fill="white", tags=('mainWindow') )

    #Bottom summary
    yLineLoc = screenSizey - 110
    canvas.create_line( int(screenSizex*.05) , yLineLoc, int(screenSizex*.95) , yLineLoc , fill="white", width=1 , tags=('mainWindow') )
    
    ySummary = yLineLoc-20
    xSummary = int(screenSizex*.15)
    summaryText = canvas.create_text(xSummary, ySummary, text=u'Status', font="Arial 25", fill="white", tags=('mainWindow') )

    bounds  = canvas.bbox(summaryText)
    xoffset = bounds[0];
    
    modeText = canvas.create_text(xSummary, ySummary+45, text=u'Standby Mode', font="Arial 25", fill="white", tags=('mainWindow', 'HVACMode') )
    bounds = canvas.bbox(modeText)  # returns a tuple like (x1, y1, x2, y2)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    bounds = canvas.bbox(modeText)
    
    canvas.coords(modeText, int(xoffset + width/2), ySummary+45 )
    
    modeText = canvas.create_text(xSummary, ySummary+90, text=u'Humidity  44%', font="Arial 25", fill="white", tags=('mainWindow', 'area1Humidity') )
    bounds = canvas.bbox(modeText)  # returns a tuple like (x1, y1, x2, y2)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    bounds = canvas.bbox(modeText)
    canvas.coords(modeText, int(xoffset + width/2), ySummary+90 )


    #if area 2 or 3 
    canvas.create_text(int(screenSizex*.60), ySummary, text=u'Area 2', font="Arial 25", fill="white", tags=('mainWindow', 'area2Name') )
    canvas.create_text(int(screenSizex*.60), ySummary+45, text=u'76\N{DEGREE SIGN}', font="Arial 25", fill="white", tags=('mainWindow', 'area2Temp') )
    canvas.create_text(int(screenSizex*.60), ySummary+90, text=u'76%', font="Arial 25", fill="white", tags=('mainWindow', 'area2Humidity') )
    
    canvas.create_text(int(screenSizex*.80), ySummary, text=u'Area 3', font="Arial 25", fill="white", tags=('mainWindow', 'area3Name') )
    canvas.create_text(int(screenSizex*.80), ySummary+45, text=u'78\N{DEGREE SIGN}', font="Arial 25", fill="white", tags=('mainWindow', 'area3Temp') )
    canvas.create_text(int(screenSizex*.80), ySummary+90, text=u'78%', font="Arial 25", fill="white", tags=('mainWindow', 'area3Humidity') )


    bindHomeScreen( canvas )
    

#Go through an bind each element for change
def bindHomeScreen( canvas ):

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
    

def drawAreaScreen( canvas, screenSizex, screenSizey ):
    clearAllScreen( canvas )
    xNameOffset = 30
    yNameOffset = 40
    areaName = canvas.create_text(xNameOffset, 0, text=u'Area Settings', font="Arial 36", fill="white", tags=('mainWindow', 'area1Name') )
    bounds = canvas.bbox(areaName)  # returns a tuple like (x1, y1, x2, y2)
    
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    canvas.coords(areaName, bounds[2], bounds[3]+yNameOffset )
    
    #(x1, y1, x2, y2)
    canvas.create_line(0, height+yNameOffset, width+100+xNameOffset ,  height+yNameOffset , fill="white", width=3 , tags=('mainWindow') )
    canvas.create_line(0, height+yNameOffset+5, width+75+xNameOffset ,  height+yNameOffset+5 , fill="white", width=1 , tags=('mainWindow') )
    
    areaDetailFunc= lambda e: drawAreaDetailScreen(canvas, screenSizex, screenSizey, 0)
    makeAreaButton( canvas, (screenSizex*.37), (screenSizey*.25), "Area Name", tags=('areasWindow'), command=areaDetailFunc)
    
    
    
def drawAreaDetailScreen( canvas, screenSizex, screenSizey, areaID ):
    clearAllScreen( canvas )
    
    xNameOffset = 30
    yNameOffset = 40
    areaName = canvas.create_text(xNameOffset, 0, text=u'Area Name', font="Arial 36", fill="white", tags=('mainWindow', 'area1Name') )
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
    

def drawSettingsScreen( canvas, screenSizex, screenSizey ):
    clearAllScreen( canvas )


if __name__ == "__main__":
    mainWindow = Tk()
    xVal = 768;
    yVal = 687;
    mainWindow.geometry(str(xVal)+"x"+str(yVal)) 
    drawHub(mainWindow)       
    mainloop()