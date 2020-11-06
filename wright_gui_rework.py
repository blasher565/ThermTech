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

def retrieve_hub():
    #retrieve data
    return
    
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
hub = Text(start_frame, width=50, borderwidth=5)
hub_label = Label(start_frame, text='Connected Devices')
status = Entry(start_frame, width=50, borderwidth=5)
status_label = Label(start_frame, text='status:')
monitor_interactions = Entry(start_frame, width=50, borderwidth=5)
monitor_interactions_label = Label(start_frame, text='messages sent:')

unassigned = Label(zone_frame, text='unassigned devices', padx=250, pady=25, relief='ridge')

area1 = Label(zone_frame, text='Area 1', relief='ridge')

area1_sensor = Label(zone_frame, text='temperature sensor')
area1_sensor_temp_actual = Entry(zone_frame, width=10, borderwidth=5)
area1_sensor_temp_actual_label = Label(zone_frame, text='actual temperature:')
area1_sensor_temp_desired = Entry(zone_frame, width=10, borderwidth=5)
area1_sensor_temp_desired_label = Label(zone_frame, text='desired temperature:')

area1_damper = Label(zone_frame, text='duct damper')
area1_damper_open = Entry(zone_frame, width=10, borderwidth=5)
area1_damper_open_label = Label(zone_frame, text='open:')
area1_damper_other = Entry(zone_frame, width=10, borderwidth=5)
area1_damper_other_label = Label(zone_frame, text='something:')

area1_parameters = Label(zone_frame, text='area parameters')
area1_param_stuff1 = Entry(zone_frame, width=10, borderwidth=5)
area1_param_stuff1_label = Label(zone_frame, text='something:')
area1_param_stuff2 = Entry(zone_frame, width=10, borderwidth=5)
area1_param_stuff2_label = Label(zone_frame, text='something:')


area2 = Label(zone_frame, text='Area 2', relief='ridge')
area2_sensor = Label(zone_frame, text='temperature sensor')
area2_sensor_temp_actual = Entry(zone_frame, width=10, borderwidth=5)
area2_sensor_temp_actual_label = Label(zone_frame, text='actual temperature:')
area2_sensor_temp_desired = Entry(zone_frame, width=10, borderwidth=5)
area2_sensor_temp_desired_label = Label(zone_frame, text='desired temperature:')

area2_damper = Label(zone_frame, text='duct damper')
area2_damper_open = Entry(zone_frame, width=10, borderwidth=5)
area2_damper_open_label = Label(zone_frame, text='open')
area2_damper_other = Entry(zone_frame, width=10, borderwidth=5)
area2_damper_other_label = Label(zone_frame, text='something:')

area2_parameters = Label(zone_frame, text='area parameters')
area2_param_stuff1 = Entry(zone_frame, width=10, borderwidth=5)
area2_param_stuff1_label = Label(zone_frame, text='something:')
area2_param_stuff2 = Entry(zone_frame, width=10, borderwidth=5)
area2_param_stuff2_label = Label(zone_frame, text='something:')

#Place widgets
ld_config.grid(row=2, column=0, padx=20, pady=10)
sv_config.grid(row=3, column=0, padx=20, pady=10)
cr_test.grid(row=4, column=0, padx=20, pady=10)
ld_test.grid(row=5, column=0, padx=20, pady=10)
mod_test.grid(row=6, column=0, padx=20, pady=10)

st_test.grid(row=0, rowspan=2, column=0, columnspan=2, padx=10, pady=10)
ps_test.grid(row=0, rowspan=2, column=2, columnspan=2, padx=10, pady=10)
hub.grid(row=3, rowspan=4, column=0, columnspan=4, padx=10, pady=10)
hub_label.grid(row=2, column=0)
status.grid(row=7, column=1, columnspan=4, padx=10, pady=10)
status_label.grid(row=7, column=0)
monitor_interactions.grid(row=8, column=1, columnspan=4, padx=10, pady=10)
monitor_interactions_label.grid(row=8, column=0)

unassigned.grid(row=0, rowspan=3, column=0, columnspan=10, padx=20, pady=25)

area1.grid(row=4, column=0)
area1_sensor.grid(row=5, column=0)
area1_sensor_temp_actual.grid(row=6, column=1, padx=10, pady=10)
area1_sensor_temp_actual_label.grid(row=6, column=0)
area1_sensor_temp_desired.grid(row=7, column=1, padx=10, pady=10)
area1_sensor_temp_desired_label.grid(row=7, column=0)

area1_damper.grid(row=5, column=3)
area1_damper_open.grid(row=6, column=4, padx=10, pady=10)
area1_damper_open_label.grid(row=6, column=3)
area1_damper_other.grid(row=7, column=4, padx=10, pady=10)
area1_damper_other_label.grid(row=7, column=3)

area1_parameters.grid(row=5, column=6)
area1_param_stuff1.grid(row=6, column=6, padx=10, pady=10)
area1_param_stuff1_label.grid(row=6, column=5)
area1_param_stuff2.grid(row=7, column=6, padx=10, pady=10)
area1_param_stuff2_label.grid(row=7, column=5)

area2.grid(row=10, column=0)
area2_sensor.grid(row=11, column=0)
area2_sensor_temp_actual.grid(row=12, column=1, padx=10, pady=10)
area2_sensor_temp_actual_label.grid(row=12, column=0)
area2_sensor_temp_desired.grid(row=13, column=1, padx=10, pady=10)
area2_sensor_temp_desired_label.grid(row=13, column=0)

area2_damper.grid(row=11, column=3)
area2_damper_open.grid(row=12, column=4, padx=10, pady=10)
area2_damper_open_label.grid(row=12, column=3)
area2_damper_other.grid(row=13, column=4, padx=10, pady=10)
area2_damper_other_label.grid(row=13, column=3)

area2_parameters.grid(row=11, column=6)
area2_param_stuff1.grid(row=12, column=6, padx=10, pady=10)
area2_param_stuff1_label.grid(row=12, column=5)
area2_param_stuff2.grid(row=13, column=6, padx=10, pady=10)
area2_param_stuff2_label.grid(row=13, column=5)


root.mainloop()
