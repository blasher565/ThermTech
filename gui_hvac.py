# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:37:22 2020

@author: Brandon Lasher
"""
from tkinter import *


def drawHVAC( parent ):
    parent.update()
    ySize = parent.winfo_height();
    xSize = parent.winfo_width();
    
    hvacCanvas = Canvas(parent, width=xSize, height=ySize, bd=0, highlightthickness=0, bg="grey")
    hvacCanvas.pack()
    #areaCanvas.create_rectangle(0,0,xSize,ySize, fill="purple")
    hvacCanvas.create_text(xSize/2,(ySize)/2, text="HVAC STUFF HERE!", font=("Arial", 12), fill="black")
    
    
    
if __name__ == "__main__":
    mainWindow = Tk()
    xVal = 400;
    yVal = 125;
    mainWindow.geometry(str(xVal)+"x"+str(yVal)) 
    drawHVAC(mainWindow)
    mainloop()