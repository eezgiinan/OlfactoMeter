import pyfirmata
import threading
import tkinter as tk

# Define the pins that the valves are connected to
valve_pin_1 = 2
valve_pin_2 = 3

# Define the Model class
class ArduinoModel:
    def __init__(self):
        self.board = None
        self.connected = False
        self.valve_states = {
            valve_pin_1: False,
            valve_pin_2: False
        }

    def connect(self, port):
        try:
            self.board = pyfirmata.Arduino(port)
            self.connected = True
            print("Arduino connected.")
        except Exception as e:
            print(e)
            self.connected = False

    def set_valve_state(self, valve_pin, state):
        self.board.digital[valve_pin].write(state)
        self.valve_states[valve_pin] = bool(state)

    def close(self):
        self.board.exit()
        self.connected = False

# Define the View class
class ArduinoView:
    def __init__(self, root):
        self.root = root
        self.valve_1_button = tk.Button(root, text="Valve 1", command=self.valve_1_callback)
        self.valve_2_button = tk.Button(root, text="Valve 2", command=self.valve_2_callback)
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_callback)
        self.valve_1_button.pack(side=tk.LEFT)
        self.valve_2_button.pack(side=tk.LEFT)
        self.pause_button.pack(side=tk.LEFT)

    def valve_1_callback(self):
        controller.set_valve_state(valve_pin_1, not controller.model.valve_states[valve_pin_1])

    def valve_2_callback(self):
        controller.set_valve_state(valve_pin_2, not controller.model.valve_states[valve_pin_2])

    def pause_callback(self):
        controller.pause_experiment()

# Define the Controller class
class ArduinoController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def set_valve_state(self, valve_pin, state):
        if self.model.connected:
            self.model.set_valve_state(valve_pin, state)
            print(f"Valve {valve_pin} state set to {state}.")
        else:
            print("Arduino not connected.")

    def pause_experiment(self):
        self.running = not self.running

    def run_experiment(self):
        while True:
            if self.running:
                # Do some experiment here using the valves
                pass
            else:
                # Wait until the experiment is unpaused
                while not self.running:
                    pass

# Define the main function
def main():
    # Create the Model, View, and Controller objects
    model = ArduinoModel()
    root = tk.Tk()
    view = ArduinoView(root)
    controller = ArduinoController(model, view)

    # Connect to the Arduino board
    model.connect("COM3") # Change this to the correct port for your board

    # Start the experiment thread
    experiment_thread = threading.Thread(target=controller.run_experiment)
    experiment_thread.daemon = True
    experiment_thread.start()

    # Start the UI mainloop
    root.mainloop()

    # Close the Arduino board connection when the UI is closed
    model.close()

if __name__ == "__main__":
    main()