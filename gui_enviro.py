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


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, kwargs, highlightthickness=0, bd=0)
        
        scrollbarV = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbarH = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbarV.set, xscrollcommand=scrollbarH.set)
        
        scrollbarV.pack(side="right", fill="y")
        scrollbarH.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
       


def drawEnv( parent ):
    parent.update()
    ySize = parent.winfo_height();
    xSize = parent.winfo_width();
    
    topFrameSize = 70;
    topFrame = LabelFrame(parent, text="Simulation Controls", bg=parent["background"])
    #topFrame.grid(row=0, column=0, sticky=E+W+S+N)
    topFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    
    bottomFrame = ScrollableFrame(parent, bg=parent["background"])
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
    sensorBox = ttk.Spinbox(addFrame, from_=0, to=4, width=5, textvariable=sensorNum, state='readonly', validate="all")
    sensorNum.set(1)
    #sensorBox.grid(row=1, column=1)
    
    addBut = Button( addFrame, text = "ADD", command=lambda: addZone(bottomFrame.scrollable_frame, 0, sensorNum.get(), damperNum.get() ))
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
    #iglu_Timer.timerVal, iglu_Timer.runTimer, iglu_Timer.timeSpeed
    #playImg = ImageTk.PhotoImage(file = r"C:/Users/brand/Documents/GitHub/ThermTech/images/playbut.png") 
    #pauseImg = ImageTk.PhotoImage(file = r"C:/Users/brand/Documents/GitHub/ThermTech/images/pausebut.png") 
    #resetImg = ImageTk.PhotoImage(file = r"C:/Users/brand/Documents/GitHub/ThermTech/images/resbut.png") 
    
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
    
    #st_test.grid(row=0, column=1, padx=2, pady=2)
    #ps_test.grid(row=0, column=2, padx=2, pady=2)
    #rs_test.grid(row=0, column=3, padx=2, pady=2)
    #speedSelect.grid(row=0, column=0, padx=2, pady=2)
    speedSelect.pack( side=LEFT )
    timeCanvas.pack( side=LEFT, expand=True )
    st_test.pack( side=LEFT )
    ps_test.pack( side=LEFT )
    rs_test.pack( side=LEFT )

    #timeCanvas.grid(row=1, column=0, columnspan=4, padx=2, pady=2)

    
    #spacerFrame = Frame(simFrame, width=50, bg=simFrame["background"])
    #spacerFrame.grid(row=0, rowspan=2, column=5, sticky=N+S)
    
    #bind the timer text change to, the counter value changing
    iglu_Timer.globalTimer.bind_to(updateTime)
    
#
# Update the time value displayed
#    
def updateTime( countValue ):    
    hours, mins = divmod(countValue, 60)
    days, hours = divmod(hours, 24)
    timer = '{:02d}:{:02d}:{:02d}'.format(days, hours, mins) 
    timeCanvas.itemconfigure(timerText, text=timer)

#create sensor object bind update funciton to it
#  This needs to be setup as a global or class
def addSensor( parentFrame ):
    parentFrame.update()
    #make generic container to hold sensor Info
    sensFrame = Frame(parentFrame, bg=parentFrame["background"], highlightthickness=2, highlightbackground="black")
    sensFrame.pack(side=LEFT)
    
    node = SN.satelliteNode("DEV2", 0)
    updateValue = node.getLastUpdate();
    
    labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
    sensText = Label(sensFrame, text=labelText, font=("Arial 8 bold underline"), bg=parentFrame["background"] )
    #sensText.grid( row=0, column=0, columnspan=2, sticky=E+W)
    sensText.pack( side=TOP, fill=X, anchor=CENTER )
    
    for idx,k in enumerate(updateValue):
        textFrame = Frame(sensFrame)
        textFrame.pack(side=TOP, fill=X)
        sensText = Label(textFrame, text=str(k) + ": ", font=("Arial 8"), bg=parentFrame["background"] ).pack( side=LEFT, anchor=CENTER )
        valText = Label(textFrame, text=str(updateValue[k]), font=("Arial 8"), bg=parentFrame["background"] ).pack( side=RIGHT, anchor=CENTER )
        

def addDamper( parentFrame ):
    parentFrame.update()
    #make generic container to hold sensor Info
    dampFrame = Frame(parentFrame, bg=parentFrame["background"], highlightthickness=2, highlightbackground="black")
    dampFrame.pack(side=LEFT)
    
    node = DA.damper("DEV1", 0)
    labelText = node.deviceType + "(" + str( node.uniqueID ) + ")"
    dampText = Label(dampFrame, text=labelText, font=("Arial 8 bold underline"), bg=parentFrame["background"] )
    dampText.grid( row=0, column=0, columnspan=2, sticky=E+W)   
    
    lblText = Label(dampFrame, text="Flow Rate: ", font=("Arial 8"), bg=parentFrame["background"] )
    lblText.grid( row=1, column=0, sticky=E)   
    
    rateText = Label(dampFrame, text=node.flowRate, font=("Arial 8"), bg=parentFrame["background"] )
    rateText.grid( row=1, column=0, sticky=E)  
    


def addZone( parentFrame, zoneID, numSensor=0, numDamper=0 ):    
    #parentFrame.update()
    zoneFrame = LabelFrame(parentFrame, width=parentFrame.winfo_width(), text="Zone " + str(zoneID), bg=parentFrame["background"] )
    zoneFrame.pack( fill=X, anchor=N )
    
    removeBut = Button(zoneFrame, width=1, text="X", font=("Arial", 12), command = lambda: removeZone(zoneFrame) )
    #removeBut.grid(row=0, rowspan=2, column=0, sticky=W)
    removeBut.pack(side=LEFT, padx=5)
    removeBut.update()
    
    sensframe = Frame( zoneFrame, height=zoneFrame.winfo_height()/2, width=zoneFrame.winfo_width()-removeBut.winfo_width(), bg=zoneFrame["background"] )
    #sensframe.grid(row=0, column=1, sticky=W+E)
    sensframe.pack(side=TOP, anchor=W)
    dampframe = Frame( zoneFrame, height=zoneFrame.winfo_height()/2, width=zoneFrame.winfo_width()-removeBut.winfo_width(), bg=zoneFrame["background"] )
    #dampframe.grid(row=1, column=1, sticky=W+E, pady=2)
    dampframe.pack(side=TOP, anchor=W)
    
    for x in range(numSensor):
        addSensor(sensframe)
        
    for x in range(numDamper):
        addDamper(dampframe)
        
    parentFrame.update()
        
        
def removeZone( parentFrame ):
    #if last zone don't delete?
    parentFrame.destroy()
    

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
    
    drawEnv(mainWindow)    
    mainloop()
    
    #ends the counter thread!
    iglu_Timer.terminate()

