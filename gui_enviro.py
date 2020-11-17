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
    
import satelliteNode as SN
import damper as DA


# class ScrollableFrame(Frame):
#     def __init__(self, container, *args, **kwargs):
#         super().__init__(container, *args, **kwargs)
#         canvas = Canvas(self, kwargs, highlightthickness=0, bd=0)
#         scrollbarV = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
#         scrollbarH = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
#         self.scrollable_frame = Frame(canvas)

#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(
#                 scrollregion=canvas.bbox("all")
#             )
#         )

#         canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

#         canvas.configure(yscrollcommand=scrollbarV.set, xscrollcommand=scrollbarH.set)
        
#         scrollbarV.pack(side="right", fill="y")
#         scrollbarH.pack(side="bottom", fill="x")
#         canvas.pack(side="left", fill="both", expand=True)


class gui_enviro:
    def __init__(self):
        self.numZones = 0
        
        
        
        
        #These always return ref to the thing itself
        self.addZoneCallback = None;     #return new zone
        self.removeZoneCallback = None;  #
        self.addSenorCallback = None;    #return new Sensor
        self.addDamperCallback = None;           #return new Damper
                
    
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
        #make generic container to hold sensor Info
        sensFrame = Frame(parentFrame, bg=parentFrame["background"], highlightthickness=2, highlightbackground="black", width=140, height=110 )
        sensFrame.pack(side=LEFT)
        sensFrame.pack_propagate(False)
        sensFrame.grid_propagate(False)
        
        #for testing make own else in simulation use defined
        if not instance:
            node = SN.satelliteNode("DEV2", 0)
        else:
            node = instance
            
        updateValue = node.getLastUpdate();
        labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
        sensText = Label(sensFrame, text=labelText, font=("Arial 8 bold underline"), bg=parentFrame["background"] )
        sensText.grid( row=0, column=0, columnspan=2, sticky=E+W)


        nodeInfo = {}               
        for rowCnt, k in enumerate(updateValue):           
            
            sensText = Label(sensFrame, text=str(k) + ": ", font=("Arial 8"), bg=parentFrame["background"] ).grid( row=rowCnt+1, column= 0, sticky=E )
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
        #make generic container to hold sensor Info
        dampFrame = Frame(parentFrame, bg=parentFrame["background"], highlightthickness=2, highlightbackground="black",  width=120, height=50)
        dampFrame.pack(side=LEFT)
        dampFrame.pack_propagate(False)
        dampFrame.grid_propagate(False)
        
        if not instance:
            node = DA.damper("DEV1", 0)
        else:
            node = instance
        
        labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
        dampText = Label(dampFrame, text=labelText, font=("Arial 8 bold underline"), bg=parentFrame["background"] )
        dampText.grid( row=0, column=0, columnspan=2, sticky=N+W+E)
        
        
        lblText = Label(dampFrame, text="Flow Rate: ", font=("Arial 8"), bg=parentFrame["background"], anchor="e"  )
        lblText.grid( row=1, column=0, sticky=W+E)
        
        rateText = Label(dampFrame, font=("Arial 8"), bg=parentFrame["background"], anchor="w" )
        self.updateDamperText( node, rateText)
        rateText.grid( row=1, column=1, sticky=W+E) 
        
        if instance:
            instance.bind_to( lambda: self.updateDamperText( node, rateText) )
        
    def updateDamperText( self, node, nodeInfo  ):
        updateValue = node.flowRate;
        nodeInfo.configure(text = '{:6.2f} %'.format(updateValue) )    
    
    def addZone(self, parentFrame, numSensor=0, numDamper=0 ): 
        
        if( self.addZoneCallback ):
            #Call the simulation add function
            # And allow it to limit the number of devices
            zone = self.addZoneCallback( numSensor=numSensor, numDamper=numDamper )
            zoneName = zone.name
        else:
            zone =  self.numZones < 4
            zoneName = "Area " + str(self.numZones)
            
        if( zone ):
            if( numSensor>0 or numDamper>0 ):
                parentFrame.update()
                zoneFrame = LabelFrame(parentFrame, text=zoneName, bg=parentFrame['background'] )
                zoneFrame.pack( side=TOP, fill=X, anchor=W )
                
                removeBut = Button(zoneFrame, width=1, text="X", font=("Arial", 12), command = lambda: self.removeZone(zoneFrame, zone) )
                removeBut.pack(side=LEFT, expand=False, padx=5)
                removeBut.update()
                
                devFrame = Frame(zoneFrame, bg=parentFrame['background'] )
                devFrame.pack(side=LEFT, fill=Y, anchor=W)
            
                if( self.addZoneCallback):
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
                    
                tempCtrlFrame = LabelFrame(zoneFrame, text="Current Temp:", bg=zoneFrame['background'], font=("Arial 8 bold underline"))
                tempCtrlFrame.pack(side=RIGHT, fill=Y, expand=False, ipadx=10)
                self.addTempControl(tempCtrlFrame)
                
                self.numZones=self.numZones+1
        else:
            #place error block
            pass
            
            
        
    def addTempControl(self, parentFrame ):
        #currentTempLabel0= Label( parentFrame, text="Current Temp:", font=("Arial 8 bold underline"), bg=parentFrame['background'])
        #currentTempLabel0.pack(expand=False, anchor=CENTER, fill=X)
        parentFrame.update()
        tempFrame = Frame(parentFrame)
        tempFrame.pack( expand=True, anchor=W, fill=X)
        
        currentTempLabel1= Label( tempFrame, text="", width=4,  bg="black", font=("Arial 10 bold"), fg="white")
        self.updateDegree(currentTempLabel1, 0)
        #unitTempLabel= Label( tempFrame, text=u'\N{DEGREE SIGN}F',  bg="black", font=("Arial 10 bold"), fg="white")
        
        upButton=Button(tempFrame, text="^", width=2, command=lambda: self.changeDegree(currentTempLabel1, 1))
        downButton=Button(tempFrame, text="v", width=2, command=lambda: self.changeDegree(currentTempLabel1, 0) )
    
        currentTempLabel1.pack( side=LEFT, fill=BOTH, expand=True, anchor=E)
        #unitTempLabel.pack( side=LEFT, fill=BOTH, expand=True, anchor=W)
        downButton.pack( side=RIGHT, fill=Y,anchor=SE)
        upButton.pack( side=RIGHT, fill=Y,anchor=NE )
    
    
    def changeDegree(self, label, direction ):
        value = int( label["text"].strip(u'\N{DEGREE SIGN} F') )
        t = -1
        if( direction ):
            t = 1
        self.updateDegree( label, value + t )
    
    
    def updateDegree(self, label, value ):
        label["text"]="{1:0{0}d}{2}".format(2 if value >=0 else 3,int(value), u'\N{DEGREE SIGN} F' )
            
    def removeZone(self, parentFrame, zone ):
        if( self.removeZoneCallback ):
            check = self.removeZoneCallback( zone );
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

