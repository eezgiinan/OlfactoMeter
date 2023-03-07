import pyfirmata
import time
from tkinter import *
from tkinter import filedialog
import pandas as pd
import enum

# Connect to the Arduino board via serial port
port = 'COM4'
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
    """
    DIfferent controls that the user can run
    """
    Start = 'Start Experiment'
    Stop = 'Stop and Close Experiment'
    DisplayData = 'Display Data'


# Initialize pins to a known state
def _init_pins():
    for pin in PINS:
        pin.mode = pyfirmata.OUTPUT
        pin.write(CLOSE)


# Define a function to set the mode and activate the corresponding pins for a certain duration
def set_mode(mode, duration):
    # Check if the mode is valid
    if mode not in Modes:
        print(f"Invalid mode: {mode}")
        return
    # Check if the duration is valid
    if duration <= 0:
        print(f"Invalid duration: {duration}")
        return
    # Get the pin values for the selected mode
    valves = mode.value
    # Activate the corresponding pins for the selected mode
    for i, valve in enumerate(PINS):
        valve.mode = pyfirmata.OUTPUT
        valve.write(valves[i])
    # Wait for the specified duration
    time.sleep(duration)
    # Deactivate all pins
    for pin in PINS:
        pin.write(CLOSE)


# Read data from the Excel file
# data = pd.read_excel('/Users/auroredelafouchardiere/PycharmProjects/firmataexcel/venv/experiment_data.xlsx')(where my file is)

# Define a function to handle the add file button click and select a file from the computer
def add_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if filename:
        global data
        data = pd.read_excel(filename)
        # Update the label to display the name of the selected file
        file_label.config(text=filename.split("/")[-1])


# Define a function to handle button clicks and activate the corresponding mode
def on_button_click(command):
    if command in Modes:
        duration = duration_var.get()
        set_mode(command, duration)
    if command == Controls.Start:
        if 'data' not in globals():
            print("Please select a data file first")
            return
        for index, row in data.iterrows():
            set_mode(Modes[row['mode'].title()], row['duration'])
    if command == Controls.Stop:
        close()


# Define a function to close the window
def close():
    window.destroy()


# Create a graphical user interface (GUI) using the Tkinter library

window = Tk()
window.geometry("600x450")

def DisplayData():
    # Create a new window
    data_window = Toplevel(window)
    data_window.title("Data")
    data_window.geometry("600x450")

    # Create a text box to display the data
    data_text = Text(data_window)
    data_text.pack(fill=BOTH, expand=YES)

    # Check if data exists
    if 'data' in globals():
        # Convert data to a string and insert it into the text box
        data_str = str(data)
        data_text.insert(END, data_str)
    else:
        # If no data exists, display a message in the text box
        data_text.insert(END, "No data available")

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
select_file_button = Button(window, text="Add File", command=add_file)
select_file_button.pack(side=BOTTOM)

# Create a label to display the name of the selected file
file_label = Label(window, text="")
file_label.pack(side=TOP)

# Display the buttons in the interface
for b in buttons:
    b.pack(side=LEFT)

# Start the main event loop for the interface
window.mainloop()
