# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 17:31:24 2020

@author: Brandon Lasher
"""
from tkinter import *

def drawHub( parent ):
    parent.update()
    ySize = parent.winfo_height();
    xSize = parent.winfo_width();
    #menuFrame_height = int(ySize *.1); 
    menuFrame_height = 24; 
    #displayFrame_height = ySize - menuFrame_height;
    displayFrame_height = ySize;
    
    #create frame
    displayFrame = Frame( parent, width=xSize, height=displayFrame_height, bg="red" )
    displayFrame.grid(row=0, column=0, sticky=N)

    menuFrame =  Frame( parent, width=xSize, height=menuFrame_height, bg="blue" )    
    menuFrame.grid(row=0, column=0, sticky=S+W)

    mainCanvas = Canvas(displayFrame, width=xSize, height=ySize, bd=0, highlightthickness=0, bg="orange")
    mainCanvas.pack(fill=BOTH)
    #mainCanvas.create_rectangle(0,0,xSize,ySize, fill="orange")
    mainCanvas.create_text(xSize/2,(ySize-menuFrame_height)/2,text="Home", font=("Arial", 12), fill="white")

    settingsCanvas = Canvas(displayFrame, width=xSize, height=ySize, bd=0, highlightthickness=0, bg="blue")
    #settingsCanvas.create_rectangle(0,0,xSize,ySize, fill="blue")
    settingsCanvas.create_text(xSize/2,(ySize-menuFrame_height)/2, text="Settings", font=("Arial", 12), fill="white")
    
    areaCanvas = Canvas(displayFrame, width=xSize, height=ySize, bd=0, highlightthickness=0, bg="green")
    #areaCanvas.create_rectangle(0,0,xSize,ySize, fill="purple")
    areaCanvas.create_text(xSize/2,(ySize-menuFrame_height)/2, text="Zones", font=("Arial", 12), fill="white")
    
    #define Menu
    global menuList
    menuList = [None]*6   
    menuList[0] = menuButton(menuFrame, "Home", (xSize/6), menuFrame_height  ).bind("<Button-1>", lambda e: setView(displayFrame, mainCanvas) )
    menuList[1] = menuButton(menuFrame, "Settings", (xSize/6) , menuFrame_height ).bind("<Button-1>", lambda e: setView(displayFrame, settingsCanvas) )
    menuList[2] = menuButton(menuFrame, "Area", (xSize/6) , menuFrame_height ).bind("<Button-1>", lambda e: setView(displayFrame, areaCanvas) )
    
    displayFrame.update()
#
#  Main window which shows temp/humid + targets
#
def setView( parent, view ):
    clearView(parent)
    view.pack( fill=BOTH )

    
def clearView( parent ):
    #parent.pack_forget()
    #parent.grid_forget()
    for widget in parent.winfo_children():
        widget.pack_forget()
 #   parent.update()
    
def menuButton( parent, value, xSize, ySize ):
    but = Canvas(parent, width=xSize, height=ySize, bd=0, highlightthickness=0)
    but.pack( side=LEFT)
    #but.create_rectangle(0, 0, xSize, ySize)
    but.create_text( xSize/2, ySize/2, text=value )
    return but  


if __name__ == "__main__":
    mainWindow = Tk()
    xVal = 400;
    yVal = 550;
    mainWindow.geometry(str(xVal)+"x"+str(yVal)) 
    drawHub(mainWindow)       
    mainloop()