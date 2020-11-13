# GUI - Iglu Termostat System

from tkinter import *
from PIL import Image, ImageTk
from gui_hub import * 
from gui_hvac import *
from gui_enviro import *
import iglu_Timer
import os


#Define root
root = Tk()

#Set title and labels
root.title('ThermTech Interior Climate Solution')


#makes both sides the same size
root.grid_columnconfigure(0, weight=1, uniform="group1")
root.grid_columnconfigure(1, weight=1, uniform="group1")
root.grid_rowconfigure(0, weight=1)
root.geometry('%sx%s' % (int(root.winfo_screenwidth() *.8), int(root.winfo_screenheight()*.8)))
root.resizable(False,False)
root.update()

comp_label = Label(text='Welcome to Iglu\nDevice Emulation Application:  Test Environment', font=("Helvetica bold", 12))
#comp_label.grid(row=0, columnspan=2, sticky=E+W)
comp_label.pack(side=TOP, fill=X, ipady=5)
comp_label.update()

#Define Both sides
#Runing time Side
frameHeight = root.winfo_height() - comp_label.winfo_height()
frameWidth = root.winfo_width() 
start_frame = Frame(root, height=frameHeight, width=int(frameWidth/2))
#start_frame.grid(row=1, column=0, sticky=W+N+S+E)
start_frame.pack(side=LEFT, anchor=CENTER, fill=BOTH)
start_frame.update()

#Area / Config side
zone_frame = Frame(root, height=frameHeight, width=frameWidth)
#zone_frame.grid(row=1, column=1, sticky=N+E+S+W)
zone_frame.pack(side=RIGHT, anchor=CENTER, fill=BOTH)
zone_frame.pack_propagate(False)

#Everything in HVAC/HUB/MESSAGE Frame 
#hub = Text(start_frame, width=50, borderwidth=5)
#hub_label = Label(start_frame, text='Connected Devices')
#status = Entry(start_frame, width=50, borderwidth=5)
#status_label = Label(start_frame, text='status:')
#monitor_interactions = Entry(start_frame, width=50, borderwidth=5)
#monitor_interactions_label = Label(start_frame, text='messages sent:')

# Start Frame is broken into top frame for HUB
# and bottom frame for HVAC
#
hub_frame = Frame(start_frame, height=frameHeight-125, width=start_frame.winfo_width())
#hub_frame.grid(row=0, column=0, sticky=W+N+S+E)
hub_frame.pack(side=TOP, anchor=N, fill=BOTH)

hvac_frame = Frame(start_frame, height=125, width=start_frame.winfo_width())
#hvac_frame.grid(row=1, column=0, sticky=W+N+S+E)
hvac_frame.pack(side=BOTTOM, anchor=S, fill=BOTH)

#start_frame.grid_rowconfigure(0, weight=0)
#start_frame.grid_rowconfigure(1, weight=1)

hub_frame.update();
drawHub(hub_frame)

hvac_frame.update()
drawHVAC(hvac_frame)

zone_frame.update()
drawEnv(zone_frame)

"""
top_frame =  Frame( zone_frame, bg="pink" )
top_frame.grid( row=0, column=0, sticky=E+W+S+N)

bottom_frame =  Frame( zone_frame, bg="brown" )
bottom_frame.grid( row=1, column=0, sticky=E+W+N+S)



#Zone
device_frame = Frame( top_frame, bg ="blue" )
#device_frame.pack( anchor=N+W, expand = False )
device_frame.grid( row=0, column=0, sticky=E)

add_area = Button ( device_frame, text="Add Area", command= lambda: addArea(bottom_frame) )
add_sens = Button ( device_frame, text="Add Sensor", command= lambda: emptyfunc() )
add_damp = Button ( device_frame, text="Add Damper", command= lambda: emptyfunc() )
add_area.grid( row = 0, column = 0, padx=5, pady=5)
add_sens.grid( row = 0, column = 1, padx=5, pady=5)
add_damp.grid( row = 0, column = 2, padx=5, pady=5)

play_frame = LabelFrame( top_frame, text="Test Controls", bg="red" )
play_frame.grid( row=0, column=1, sticky=W)

playImg = ImageTk.PhotoImage(file = r"../images/playbut.png") 
pauseImg = ImageTk.PhotoImage(file = r"../images/pausebut.png") 
st_test = Button(play_frame, text="Play", image=playImg, command= lambda: start_test())
ps_test = Button(play_frame, text="Pause", image=pauseImg, command= lambda: pause_test())
st_test.grid(row=0, column=0, padx=2, pady=5)
ps_test.grid(row=0, column=1, padx=2, pady=5)


def addArea(parent):
    ll=Label(parent, text="HWLLO WORLD!")
    ll.pack()
    ll.bind("<Button-1>", lambda e: ll.pack_forget())
    
    
def addSenor(parent):
    ll=canvas(parent, text="HWLLO WORLD!")
    ll.pack()
    ll.bind("<Button-1>", lambda e: ll.pack_forget())
"""



#Menu definitions and functions
#   Menu was added to allow for more area for display 

#Define functions for test environment
def load_config():
    pass

def save_config():
    pass

def create_test():
    pass

def load_test():
    pass

def modify_test():
    pass

def start_test():
    pass

def pause_test():
    pass

def retrieve_hub():
    #retrieve data
    pass

def emptyfunc():
    pass


mainmenu = Menu(root)

configMenu = Menu(mainmenu, tearoff = 0)
configMenu.add_command(label = "New", command = emptyfunc)
configMenu.add_command(label = "Load", command = load_config)
configMenu.add_command(label = "Save", command = save_config)
configMenu.add_command(label = "View Messages", command = emptyfunc)
mainmenu.add_cascade(label="Configuration", menu=configMenu)


testMenu = Menu(mainmenu, tearoff = 0)
testMenu.add_command(label = "Create", command = create_test)
testMenu.add_command(label = "Load", command = load_test)
testMenu.add_command(label = "Modify", command = modify_test)
mainmenu.add_cascade(label="Testing", menu=testMenu)


helpMenu = Menu(mainmenu, tearoff = 0)
helpMenu.add_command(label = "Documentation", command = emptyfunc)
mainmenu.add_cascade(label = "Help", menu = helpMenu)

mainmenu.add_command(label = "Exit", command=root.destroy)  

root.config(menu = mainmenu)

root.mainloop()
iglu_Timer.terminate()
