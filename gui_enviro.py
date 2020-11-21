# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:36:58 2020

@author: Brandon Lasher
"""

from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import time
import iglu_Timer
import iglu_hub
    
import satelliteNode as SN
import damper as DA

class gui_enviro:
    def __init__(self):
        self.numZones = 0        
        self.hub = None
                
    
    def drawEnv(self, parent ):
        parent.update()
        ySize = parent.winfo_height();
        xSize = parent.winfo_width();
        
        topFrameSize = 70;
        topFrame = LabelFrame(parent, text="Simulation Controls", bg=parent["background"])
        #topFrame.grid(row=0, column=0, sticky=E+W+S+N)
        topFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
        
        #bottomFrame = Frame(parent, bg=parent["background"])
        bottomFrame = Frame(parent, bg=parent["background"])
        bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=True, anchor=NW)
        #bottomFrame.grid(row=1, column=0, sticky=W+E+N+S)
        
        
        #
        #Define items in the top frame
        #
        #
        # For the These are for the zone addition frame
        #
        
        simFrame = Frame( topFrame, height=topFrameSize, bg=topFrame["background"])
        simFrame.pack(side=LEFT, fill=BOTH )  
        
        ttk.Separator(topFrame, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=5)
        
        addFrame = Frame( topFrame, height=topFrameSize)
        addFrame.pack(side=LEFT, fill=BOTH )
    
        
        damperLabel = Label(addFrame,text="# Dampers" )
        #damperLabel.grid(row=0, column=2)
        
        sensorLabel = Label(addFrame,text="# Sensors" )
        #sensorLabel.grid(row=0, column=1)
        
        damperNum = IntVar()
        damperBox = ttk.Spinbox(addFrame, from_=0, to=2, width=5, textvariable=damperNum, state='readonly', validate="all")
        damperNum.set(1)
        #damperBox.grid(row=1, column=2)
        
        sensorNum = IntVar()
        sensorBox = ttk.Spinbox(addFrame, from_=0, to=3, width=5, textvariable=sensorNum, state='readonly', validate="all")
        sensorNum.set(1)
        #sensorBox.grid(row=1, column=1)
        addBut = Button( addFrame, text = "ADD", command=lambda: self.addZone(bottomFrame, sensorNum.get(), damperNum.get() ))
        #addBut.grid(row=0, column=0, columnspan=1, rowspan=2, sticky=N+S+E+W, ipadx=20)   
        
        sensorLabel.pack(side=LEFT)
        sensorBox.pack(side=LEFT)
        damperLabel.pack(side=LEFT)
        damperBox.pack(side=LEFT)
        addBut.pack(side=LEFT, ipadx=5, padx=2)
        
    
        #
        # Define Items in the simulation frame
        #  These display and start, stop and reset the simulation timer
        #
        
        global  playImg, pauseImg, resetImg, timerText, timeCanvas
        playImg = ImageTk.PhotoImage(file = r"./images/playbut.png") 
        pauseImg = ImageTk.PhotoImage(file = r"./images/pausebut.png") 
        resetImg = ImageTk.PhotoImage(file = r"./images/resbut.png") 
    
        st_test = Button(simFrame, text="Play", image=playImg, bd=1, highlightthickness=1, command= lambda: iglu_Timer.globalTimer.startCounter() )
        ps_test = Button(simFrame, text="Pause", image=pauseImg, bd=1, highlightthickness=1, command= lambda: iglu_Timer.globalTimer.pauseCounter() )
        rs_test = Button(simFrame, text="Restart", image=resetImg, bd=1, highlightthickness=1, command= lambda: iglu_Timer.globalTimer.restartCounter() )
        
        menuOpts = {"x1 ":1,"x5 ":5,"x10":10,"x20":20, "x200":200, "x1000":1000}
        variable = StringVar(simFrame)
        variable.set("x1") # default value
        
        speedSelect = OptionMenu(simFrame,  variable, *menuOpts.keys())
        variable.trace('w', lambda *args: iglu_Timer.globalTimer.updateSpeed(menuOpts[variable.get()]) )
        
    
        st_test.config(width=30)
        ps_test.config(width=30)
        rs_test.config(width=30)
        speedSelect.config(width=5)
    
        timeCanvas = Canvas( simFrame, height=playImg.height(), width=100, bd=0, highlightthickness=0, bg="black" )
        timerText = timeCanvas.create_text(50,playImg.height()/2, text=str("00:00:00"), font=("Arial", 12), fill="white") 
        
        speedSelect.pack( side=LEFT )
        timeCanvas.pack( side=LEFT)
        st_test.pack( side=LEFT )
        ps_test.pack( side=LEFT )
        rs_test.pack( side=LEFT )
    
        
        #bind the timer text change to, the counter value changing
        iglu_Timer.globalTimer.bind_to(self.updateTime)
        
        
        if self.hub:
            for a in self.hub.areaList:
                self.addZone(bottomFrame, 1, 0, a, static=True)
            
        
    #
    # Update the time value displayed
    #    
    def updateTime(self, countValue ):    
        hours, mins = divmod(countValue, 60)
        days, hours = divmod(hours, 24)
        timer = '{:02d}:{:02d}:{:02d}'.format(days, hours, mins) 
        timeCanvas.itemconfigure(timerText, text=timer)
    
    #create sensor object bind update funciton to it
    #  This needs to be setup as a global or class
    def addSensor(self, parentFrame, instance ):
        parentFrame.update()
        
        #for testing make own else in simulation use defined
        if not instance:
            node = SN.satelliteNode("DEV2", 0)
        else:
            node = instance
            
        updateValue = node.getLastUpdate();
        
        #make generic container to hold sensor Info
        labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
        sensFrame = LabelFrame(parentFrame, bg=parentFrame["background"], text=labelText, highlightthickness=0, highlightbackground="black", font=("Arial 8 bold underline"), borderwidth=2, width=140, height=110 )
        sensFrame.pack(side=LEFT)
        sensFrame.pack_propagate(False)
        sensFrame.grid_propagate(False)
        sensFrame.columnconfigure(0, weight = 0)
        sensFrame.columnconfigure(1, weight = 1)

        #labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
        #sensText = Label(sensFrame, text=labelText, font=("Arial 8 bold underline"), bg=parentFrame["background"] )
        #sensText.grid( row=0, column=0, columnspan=2, sticky=E+W)

        nodeInfo = {}               
        for rowCnt, k in enumerate(updateValue):           
            
            sensText = Label(sensFrame, text=str(k) + ": ", font=("Arial 10"), bg=parentFrame["background"] ).grid( row=rowCnt+1, column= 0, sticky=E )
            valText = Label(sensFrame, font=("Arial 8"), bg=parentFrame["background"] )
            valText.grid( row=rowCnt+1, column= 1, sticky=W )
                        
            nodeInfo[str(k)] = valText;
            self.updateSensorText( node, nodeInfo)
            
        if instance:
            instance.bind_to( lambda: self.updateSensorText( node, nodeInfo) )
    
    
    def updateSensorText( self, node, nodeInfo  ):
        updateValue = node.getLastUpdate();
        for k in nodeInfo:
            for i in updateValue:
                if k == str(i):
                    #print(updateValue[i][0])
                    if updateValue[i][0] == None:
                        nodeInfo[k].configure( text = "None" )    
                    else:
                        nodeInfo[k].configure( text = updateValue[i][1].format(updateValue[i][0][1]) )
                    break
                    
            # sensText = Label(textFrame, text=str(k) + ": ", font=("Arial 8"), bg=parentFrame["background"] ).pack( side=LEFT, anchor=CENTER )
            # valText = Label(textFrame, text=str(updateValue[k]), font=("Arial 8"), bg=parentFrame["background"] ).pack( side=RIGHT, anchor=CENTER )

                   
        
    
    def addDamper(self, parentFrame, instance ):
        parentFrame.update()
        
        if not instance:
            node = DA.damper("DEV1", 0)
        else:
            node = instance
        
        labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
        
        #make generic container to hold sensor Info
        dampFrame = LabelFrame(parentFrame, bg=parentFrame["background"], text=labelText, highlightthickness=0, highlightbackground="black", font=("Arial 8 bold underline"), borderwidth=2, width=120, height=45 )
        dampFrame.pack(side=LEFT)
        dampFrame.pack_propagate(False)
        dampFrame.grid_propagate(False)
        dampFrame.columnconfigure(0, weight = 0)
        dampFrame.columnconfigure(1, weight = 1)

        

        #dampText = Label(dampFrame, text=labelText, font=("Arial 8 bold underline"), bg=parentFrame["background"] )
        #dampText.grid( row=0, column=0, columnspan=2, sticky=N+W+E)
        
        
        lblText = Label(dampFrame, text="Flow Rate: ", font=("Arial 8"), bg=parentFrame["background"], anchor="e"  )
        lblText.grid( row=0, column=0, sticky=W+E)
        
        rateText = Label(dampFrame, font=("Arial 8"), bg=parentFrame["background"], anchor="w" )
        self.updateDamperText( node, rateText)
        rateText.grid( row=0, column=1, sticky=W+E) 
        
        if instance:
            instance.bind_to( lambda: self.updateDamperText( node, rateText) )
        
    def updateDamperText( self, node, nodeInfo  ):
        updateValue = node.flowRate;
        nodeInfo.configure(text = '{:6.2f} %'.format(updateValue) )    
    
    def addZone(self, parentFrame, numSensor=0, numDamper=0, exisitingArea=None, static=False ): 
        parentFrame.update()
        if not( exisitingArea ):
            if( self.hub ):
                #Call the simulation add function
                # And allow it to limit the number of devices
                zone = self.hub.addArea( numSensor=numSensor, numDamper=numDamper )
                if zone:
                    zoneName = zone.name
                else:
                    zoneName = "Area " + str(self.numZones) #if fail to add
            else:
                zone =  self.numZones < 4          
                zoneName = "Area " + str(self.numZones)
        else:
            zone = exisitingArea
            zoneName = zone.name
            
            
        if( zone ):
            if( numSensor>0 or numDamper>0 ):
                parentFrame.update()
                zoneFrame = LabelFrame(parentFrame, text=zoneName, bg=parentFrame['background'] )
                zoneFrame.pack( side=TOP, fill=X, anchor=W )
                zoneFrame.columnconfigure(1, weight=1)
                
                removeBut = Button(zoneFrame, width=1, text="X", font=("Arial", 12), command = lambda: (not static) and self.removeZone(zoneFrame, zone)  )
                #removeBut.pack(side=LEFT, expand=False, padx=5)
                removeBut.grid( column= 0, row=0, padx=5)
                removeBut.update()
                
                devFrame = Frame(zoneFrame, bg=parentFrame['background'] )
                #devFrame.pack(side=LEFT, fill=Y, anchor=W)
                devFrame.grid( column= 1, row=0, sticky=W)
            
                if( self.hub ):
                    sensframe = Frame( devFrame, height=zoneFrame.winfo_height()/2, width=zoneFrame.winfo_width()-removeBut.winfo_width(), bg=zoneFrame["background"] )
                    sensframe.pack(side=TOP, anchor=W)
                    dampframe = Frame( devFrame, height=zoneFrame.winfo_height()/2, width=zoneFrame.winfo_width()-removeBut.winfo_width(), bg=zoneFrame["background"] )
                    dampframe.pack(side=TOP, anchor=W)
                    
                    for x in zone.deviceList:
                        if isinstance( x, SN.satelliteNode ):
                            self.addSensor(sensframe, x)
                            
                        if isinstance( x, DA.damper ):
                            self.addDamper(dampframe, x)
                    
                else:
                    #if no callback create dummies
                    if numSensor>0:
                        sensframe = Frame( devFrame, height=zoneFrame.winfo_height()/2, width=zoneFrame.winfo_width()-removeBut.winfo_width(), bg=zoneFrame["background"] )
                        #sensframe.grid(row=0, column=1, sticky=W+E)
                        sensframe.pack(side=TOP, anchor=W)
                        for x in range(numSensor):
                                self.addSensor(sensframe, None)
                    
                    if numDamper>0:
                        dampframe = Frame( devFrame, height=zoneFrame.winfo_height()/2, width=zoneFrame.winfo_width()-removeBut.winfo_width(), bg=zoneFrame["background"] )
                        #dampframe.grid(row=1, column=1, sticky=W+E, pady=2)
                        dampframe.pack(side=TOP, anchor=W)
                        for x in range(numDamper):
                            self.addDamper(dampframe, None)
                            
                #add to all
                tempCtrlFrame = LabelFrame(zoneFrame, text="Controls", font=("Arial 8 bold underline"))
                #tempCtrlFrame.pack(side=RIGHT, fill=Y, expand=False, ipadx=10)
                tempCtrlFrame.grid( column= 2, row=0, sticky=E+N+S)
                self.addTempControl(tempCtrlFrame, zone)
            
                self.numZones=self.numZones+1
        else:
            #place error block
            pass
            
            
        
    def addTempControl(self, parentFrame, zone ):
        #currentTempLabel0= Label( parentFrame, text="Current Temp:", font=("Arial 8 bold underline"), bg=parentFrame['background'])
        #currentTempLabel0.pack(expand=False, anchor=CENTER, fill=X)

        def incCurrentTemp(zone):
            zone.currentTempatureActual = zone.currentTempatureActual + 1
            
        def decCurrentTemp(zone):
            zone.currentTempatureActual = zone.currentTempatureActual - 1
            
        def incTargetTemp(zone):
            zone.targetTempature = zone.targetTempature + 1
            
        def decTargetTemp(zone):
            zone.targetTempature = zone.targetTempature - 1
            
        def setHvacRate(zone, rate):
            zone.hvacTempatureChangeRate = float(rate)
            
        def setTempRate(zone, rate):
            zone.externalTempatureChangeRate = float(rate)
        
        parentFrame.update()

        parentFrame.columnconfigure(1, weight=1)
        parentFrame.rowconfigure(0, weight=1)
        parentFrame.rowconfigure(1, weight=1)        
        parentFrame.rowconfigure(2, weight=1)
        parentFrame.rowconfigure(4, weight=1)

        currentTempLabel = Label( parentFrame, text="C:", width=2,  bg=parentFrame["background"], font=("Arial 10 bold"), fg="black")
        targetTempLabel = Label( parentFrame, text="T:", width=2,  bg=parentFrame["background"], font=("Arial 10 bold"), fg="black")
        rateLabel = Label( parentFrame, text="RX:", width=2,  bg=parentFrame["background"], font=("Arial 10 bold"), fg="black" )
        rateLabel1 = Label( parentFrame, text="RH:", width=2,  bg=parentFrame["background"], font=("Arial 10 bold"), fg="black" )
        
        currentTempLabel1= Label( parentFrame, text="", width=4,  bg="black", font=("Arial 10 bold"), fg="white")
        currentTempLabel2= Label( parentFrame, text="", width=4,  bg="black", font=("Arial 10 bold"), fg="white")
        tempRate = DoubleVar()
        hvacRate = DoubleVar()
        currentTempLabel3 = Scale( parentFrame, orient=HORIZONTAL, variable = tempRate, tickinterval=.01, from_=0, to=.2, resolution=.05, command=lambda r: setTempRate(zone, r) )
        currentTempLabel4 = Scale( parentFrame, orient=HORIZONTAL, variable = hvacRate, tickinterval=.01, from_=0, to=.5, resolution=.05, command=lambda r: setHvacRate(zone, r) )
        
        #set initial values
        if( self.hub ):
            tempRate.set(zone.externalTempatureChangeRate)
            hvacRate.set(zone.hvacTempatureChangeRate)

        
        self.updateDegree(currentTempLabel1, round(zone.currentTempatureActual) if self.hub else 70 )
        self.updateDegree(currentTempLabel2, round(zone.targetTempature) if self.hub else 70 )

            
        upButtonC=Button(parentFrame, text="^", width=2, command=lambda: self.hub and incCurrentTemp(zone) )
        downButtonC=Button(parentFrame, text="v", width=2, command=lambda: self.hub and decCurrentTemp(zone) )
        
        upButtonT=Button(parentFrame, text="^", width=2, command=lambda: self.hub and incTargetTemp(zone) )
        downButtonT=Button(parentFrame, text="v", width=2, command=lambda: self.hub and decTargetTemp(zone) )
    
        if( self.hub ):
            zone.bind_to_tag( ("hub_gui", "currentTempatureActual" ), lambda: self.updateDegree(currentTempLabel1, zone.currentTempatureActual) )
            zone.bind_to_tag( ("hub_gui", "targetTempature" ), lambda: self.updateDegree(currentTempLabel2, zone.targetTempature) )
            zone.bind_to_tag( ("hub_gui", "externalTempatureChangeRate" ), lambda: tempRate.set(zone.externalTempatureChangeRate) )
            zone.bind_to_tag( ("hub_gui", "hvacTempatureChangeRate" ), lambda: hvacRate.set(zone.hvacTempatureChangeRate) )
    
        currentTempLabel.grid(row=0, column=0)
        currentTempLabel1.grid(row=0, column=1)
        #unitTempLabel.pack( side=LEFT, fill=BOTH, expand=True, anchor=W)
        downButtonC.grid(row=0, column=3)
        upButtonC.grid(row=0, column=2)
        
        targetTempLabel.grid(row=1, column=0)
        currentTempLabel2.grid(row=1, column=1)
        #unitTempLabel.pack( side=LEFT, fill=BOTH, expand=True, anchor=W)
        downButtonT.grid(row=1, column=3)
        upButtonT.grid(row=1, column=2)
        
        rateLabel.grid(row=3, column=0)
        currentTempLabel3.grid(row=3, column=1, columnspan=3)
        
        rateLabel1.grid(row=2, column=0)
        currentTempLabel4.grid(row=2, column=1, columnspan=3)
    
    
    
    def updateDegree(self, label, value ):
        label["text"]="{1:0{0}d}{2}".format(2 if value >=0 else 3,int(value), u'\N{DEGREE SIGN} F' )
            
    def removeZone(self, parentFrame, zone ):
        if( self.hub ):
            check = self.hub.delArea( zone );
        else:
            check = (self.numZones > 0)
            
        #if last zone don't delete?
        if check:
            parentFrame.destroy()
            self.numZones=self.numZones-1


def emptyFunc():
    pass
    
    
if __name__ == "__main__":
    mainWindow = Tk()
    xVal = 600;
    yVal = 600;
    mainWindow.geometry(str(xVal)+"x"+str(yVal)) 
    mainWindow.configure(bg="red")
    mainWindow.grid_propagate(False)
    mainWindow.pack_propagate(False)
    
    gui = gui_enviro()
    gui.drawEnv(mainWindow)    
    
    mainWindow.mainloop()
    
    #ends the counter thread!
    iglu_Timer.terminate()

