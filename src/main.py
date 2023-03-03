import pyfirmata
import time
from tkinter import *
from tkinter import filedialog
import pandas as pd
import enum
from enum import Enum
import start_Experiment
import set_mode
import close
import DisplayData
import add_file


# Connect to the Arduino board via serial port
port = '/dev/cu.usbmodem1101'
board = pyfirmata.Arduino(port)

# Define the pins used to control the scent delivery system
# These pins are connected to relays that activate the corresponding odor valves
SA_pin = board.get_pin('d:4:o')
SB_pin = board.get_pin('d:5:o')
S1_pin = board.get_pin('d:6:o')
S2_pin = board.get_pin('d:7:o')

PINS = [SA_pin, SB_pin, S1_pin, S2_pin]

# Define the different modes of operation and the corresponding pin values
# 0 ON / 1 OFF
CLOSE = 1
OPEN = 0

class Modes(enum.Enum):
    """
    Enumeration of the different modes that the system can be IN
    """
    Resting = (CLOSE, CLOSE, CLOSE, CLOSE)  # No valves activated
    Purging = (OPEN, OPEN, CLOSE, CLOSE)  # Valve S1 and S2 activated to purge the system
    Odor_1 = (OPEN, CLOSE, OPEN, CLOSE)  # Valve SB and S1 activated to deliver odor 1
    Odor_2 = (OPEN, CLOSE, CLOSE, OPEN)  # Valve SB and S2 activated to deliver odor 2
    # The XLSX file needs to have the same names as in line 94, you call the function with user input


class Controls(enum.Enum):
    Start = 'Start Experiment'
    Stop = 'Stop and Close Experiment'
    DisplayData = 'Display Data'


# Initialize pins to a known state
def _init_pins():
    for pin in PINS:
        pin.mode = pyfirmata.OUTPUT
        pin.write(CLOSE)



# Define a function to handle button clicks and activate the corresponding mode
def on_button_click(command):
    if command in Modes:
        duration = duration_var.get()
        set_mode(command, duration)
    if command == Controls.Start:
        start_Experiment()
    if command == Controls.Stop:
        close()



# Create a graphical user interface (GUI) using the Tkinter library

window = Tk()
window.geometry("600x450")


# Create buttons for each mode of operation and associate them with the corresponding function
buttons = [Button(window, text=x.name.replace('_', ' '), command=lambda: on_button_click(x)) for x in Modes]
buttons.extend([Button(window, text=str(x.value), command=lambda: on_button_click(x)) for x in Controls])

# Create a label and an entry box to allow the user to set the duration for each mode
duration_label = Label(window, text="Duration (seconds):")
duration_label.pack(side=TOP)
duration_var = IntVar()
duration_entry = Entry(window, textvariable=duration_var)
duration_entry.pack(side=TOP)

# Create a button to select a file
select_file_button = Button(window, text="Add File", command=lambda:add_file())
select_file_button.pack(side=BOTTOM)

# Create a label to display the name of the selected file
file_label = Label(window, text="")
file_label.pack(side=TOP)

# Display the buttons in the interface
for b in buttons:
    b.pack(side=LEFT)

# Start the main event loop for the interface
window.mainloop()

