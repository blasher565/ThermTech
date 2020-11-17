
# -*- coding: utf-8 -*-
"""
# GUI - Iglu Termostat System
Created on Sun Nov 15 11:01:09 2020

@author: Brandon Lasher

gui_main is an object that will create and start the main
 gui module

"""
import threading
import time

from tkinter import *
from PIL import Image, ImageTk
from gui_hub import * 
from gui_hvac import *
from gui_enviro import *
import iglu_Timer
import os



class gui_main():
    def __init__(self ):

    
        #setup the initial Window
        self.root = Tk()
        self.gui_env = gui_enviro()
        self.gui_hub = gui_hub()  
        
        
        self.root.title('ThermTech Interior Climate Solution')
        self.root.grid_columnconfigure(0, weight=1, uniform="group1")
        self.root.grid_columnconfigure(1, weight=1, uniform="group1")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.geometry('%sx%s' % (int(self.root.winfo_screenwidth() *.8), int(self.root.winfo_screenheight()*.8)))
        self.root.resizable(False,False)
        self.root.update()
        
        comp_label = Label(text='Welcome to Iglu\nDevice Emulation Application:  Test Environment', font=("Helvetica bold", 12))
        comp_label.pack(side=TOP, fill=X, ipady=5)
        comp_label.update()

        #Define Both sides
        #Runing time Side
        frameHeight = self.root.winfo_height() - comp_label.winfo_height()
        frameWidth = self.root.winfo_width() 
        self.start_frame = Frame(self.root, height=frameHeight, width=int(frameWidth/2))
        self.start_frame.pack(side=LEFT, anchor=CENTER, fill=BOTH)
        self.start_frame.update()

        #Area / Config side
        self.zone_frame = Frame(self.root, height=frameHeight, width=frameWidth)
        self.zone_frame.pack(side=RIGHT, anchor=CENTER, fill=BOTH)
        self.zone_frame.pack_propagate(False)


        # Start Frame is broken into top frame for HUB
        # and bottom frame for HVAC
        #
        self.hub_frame = Frame(self.start_frame, height=frameHeight-125, width=self.start_frame.winfo_width())
        self.hub_frame.pack(side=TOP, anchor=N, fill=BOTH)
        
        self.hvac_frame = Frame(self.start_frame, height=125, width=self.start_frame.winfo_width())
        self.hvac_frame.pack(side=BOTTOM, anchor=S, fill=BOTH)
        
        
        self.hub_frame.update();
        self.gui_hub.drawHub(self.hub_frame)
        
        self.hvac_frame.update()
        drawHVAC(self.hvac_frame)
        
        self.zone_frame.update()
        self.gui_env.drawEnv( self.zone_frame )


        self.mainmenu = Menu(self.root)
        
        configMenu = Menu(self.mainmenu, tearoff = 0)
        configMenu.add_command(label = "New", command = self.emptyfunc)
        configMenu.add_command(label = "Load", command = self.load_config)
        configMenu.add_command(label = "Save", command = self.save_config)
        configMenu.add_command(label = "View Messages", command = self.emptyfunc)
        self.mainmenu.add_cascade(label="Configuration", menu=configMenu)
        
        
        testMenu = Menu(self.mainmenu, tearoff = 0)
        testMenu.add_command(label = "Create", command = self.create_test)
        testMenu.add_command(label = "Load", command = self.load_test)
        testMenu.add_command(label = "Modify", command = self.modify_test)
        self.mainmenu.add_cascade(label="Testing", menu=testMenu)
        
        
        helpMenu = Menu(self.mainmenu, tearoff = 0)
        helpMenu.add_command(label = "Documentation", command = self.emptyfunc)
        self.mainmenu.add_cascade(label = "Help", menu = helpMenu)
        
        self.mainmenu.add_command(label = "Exit", command=self.root.destroy)  
        
        self.root.config(menu = self.mainmenu)
        
        
    #Menu definitions and functions
    #   Menu was added to allow for more area for display 
    
    #Define functions for test environment
    def load_config(self):
        pass
    
    def save_config(self):
        pass
    
    def create_test(self):
        pass
    
    def load_test(self):
        pass
    
    def modify_test(self):
        pass
    
    def emptyfunc(self):
        pass
    
    def startUI(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = gui_main()
    gui.startUI()
    iglu_Timer.terminate()
