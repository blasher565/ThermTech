# GUI - Iglu Termostat System

from tkinter import *

#Define root
root = Tk()

#Set title and labels
root.title('ThermTech Interior Climate Solution')
comp_label = Label(text='Welcome to Iglu\nDevice Emulation Application:  Test Environment')

comp_label.grid(row=0, column=8)

start_frame = LabelFrame(root, text='Runtime')
start_frame.grid(row=1, rowspan=5, column = 1, columnspan=5)

#Define functions for test environment
def load_config():
    return

def save_config():
    return

def create_test():
    return

def load_test():
    return

def modify_test():
    return

def start_test():
    return

def pause_test():
    return

def open_hub():
    hub_window = Toplevel(root)
    hub_window.title('hub activity')
    hub_window.geometry('1000x1000')
    Label(hub_window, text='we will put hub stuff here').pack()
    
def open_monitor():
    monitor_window = Toplevel(root)
    monitor_window.title('monitor interactions')
    monitor_window.geometry('400x400')
    Label(monitor_window, text='messages sent').pack()

def open_sensor_one():
    sensor_window = Toplevel(root)
    sensor_window.title('sensor summary')
    sensor_window.geometry('400x400')
    Label(sensor_window, text='we will put summary info here').pack()
    
def open_damper_one():
    sensor_window = Toplevel(root)
    sensor_window.title('damper summary')
    sensor_window.geometry('400x400')
    Label(sensor_window, text='we will put summary info here').pack()
    
def open_param_one():
    sensor_window = Toplevel(root)
    sensor_window.title('parameters')
    sensor_window.geometry('400x400')
    Label(sensor_window, text='we will put summary info here').pack()
    
def open_sensor_two():
    sensor_window = Toplevel(root)
    sensor_window.title('sensor summary')
    sensor_window.geometry('400x400')
    Label(sensor_window, text='we will put summary info here').pack()
    
def open_damper_two():
    sensor_window = Toplevel(root)
    sensor_window.title('damper summary')
    sensor_window.geometry('400x400')
    Label(sensor_window, text='we will put summary info here').pack()
    
def open_param_two():
    sensor_window = Toplevel(root)
    sensor_window.title('parameters')
    sensor_window.geometry('400x400')
    Label(sensor_window, text='we will put summary info here').pack()

#Define frames
set_frame = LabelFrame(root, text='Settings')
set_frame.grid(row=1, column=0, padx=25, pady=50)

start_frame = LabelFrame(root, text='Runtime')
start_frame.grid(row=1, column=1, columnspan=4, padx=25, pady=50)

zone_frame = LabelFrame(root, text='Zoning')
zone_frame.grid(row=1, column=8, columnspan=10, padx=25, pady=50)



#Define buttons for test environment
ld_config = Button(set_frame, text='load config', padx=9, pady=25, command= lambda: load_config())
sv_config = Button(set_frame, text='save config', padx=9, pady=25, command= lambda: save_config())
cr_test = Button(set_frame, text='create test', padx=12, pady=25, command= lambda: create_test())
ld_test = Button(set_frame, text='load test', padx=17, pady=25, command= lambda: load_test())
mod_test = Button(set_frame, text='modify test', padx=9, pady=25, command= lambda: modify_test())

st_test = Button(start_frame, text='start test', padx=20, pady=20, command= lambda: start_test())
ps_test = Button(start_frame, text='pause test', padx=20, pady=20, command= lambda: pause_test())
hub = Button(start_frame, text='hub', padx=110, pady=100, command= lambda: open_hub())
monitor_interactions = Button(start_frame, text='monitor_ineractions', padx=75, pady=20, command= lambda: open_monitor())

unassigned = Label(zone_frame, text='unassigned devices', padx=250, pady=25, relief='ridge')

area1 = Label(zone_frame, text='Area 1', relief='ridge')
area1_sensor = Label(zone_frame, text='temperature sensor')
area1_sensor_gui = Button(zone_frame, text='summary', padx=10, pady=20, command= lambda: open_sensor_one())
area1_damper = Label(zone_frame, text='duct damper')
area1_damper_gui = Button(zone_frame, text='summary', padx=10, pady=20, command= lambda: open_damper_one())
area1_parameters = Label(zone_frame, text='area parameters')
area1_param_gui = Button(zone_frame, text='summary', padx=10, pady=20, command= lambda: open_param_one())


area2 = Label(zone_frame, text='Area 2', relief='ridge')
area2_sensor = Label(zone_frame, text='temperature sensor')
area2_sensor_gui = Button(zone_frame, text='summary', padx=10, pady=20, command= lambda: open_sensor_two())
area2_damper = Label(zone_frame, text='duct damper')
area2_damper_gui = Button(zone_frame, text='duct damper', padx=10, pady=20, command= lambda: open_damper_two())
area2_parameters = Label(zone_frame, text='area parameters')
area2_param_gui = Button(zone_frame, text='summary', padx=10, pady=20, command= lambda: open_param_two())

#Place widgets
ld_config.grid(row=2, column=0, padx=20, pady=10)
sv_config.grid(row=3, column=0, padx=20, pady=10)
cr_test.grid(row=4, column=0, padx=20, pady=10)
ld_test.grid(row=5, column=0, padx=20, pady=10)
mod_test.grid(row=6, column=0, padx=20, pady=10)

st_test.grid(row=0, rowspan=2, column=0, columnspan=2, padx=20, pady=20)
ps_test.grid(row=0, rowspan=2, column=2, columnspan=2, padx=20, pady=20)
hub.grid(row=2, rowspan=4, column=0, columnspan=4, padx=20, pady=20)
monitor_interactions.grid(row=6, rowspan=2, column=0, columnspan=4, padx=20, pady=20)

unassigned.grid(row=0, rowspan=3, column=0, columnspan=10, padx=20, pady=25)

area1.grid(row=4, column=0)
area1_sensor.grid(row=5, column=0)
area1_sensor_gui.grid(row=6, column=0, padx=20, pady=20)
area1_damper.grid(row=5, column=3)
area1_damper_gui.grid(row=6, column=3, padx=20, pady=20)
area1_parameters.grid(row=5, column=6)
area1_param_gui.grid(row=6, column=6, padx=20, pady=20)

area2.grid(row=10, column=0)
area2_sensor.grid(row=11, column=0)
area2_sensor_gui.grid(row=12, column=0, padx=20, pady=20)
area2_damper.grid(row=11, column=3)
area2_damper_gui.grid(row=12, column=3, padx=20, pady=20)
area2_parameters.grid(row=11, column=6)
area2_param_gui.grid(row=12, column=6, padx=20, pady=20)


root.mainloop()
