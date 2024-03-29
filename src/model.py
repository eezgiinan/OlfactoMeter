import datetime
import pyfirmata
from pandas import DataFrame
from modes import *


class Olfactometer:
    def __init__(self, port):
        self.port = port
        self.board = pyfirmata.Arduino(port)
        print(port)
        self.SA_pin = self.board.get_pin('d:4:o')
        self.SB_pin = self.board.get_pin('d:5:o')
        self.S1_pin = self.board.get_pin('d:6:o')
        self.S2_pin = self.board.get_pin('d:7:o')

        self.PINS = [self.SA_pin, self.SB_pin, self.S1_pin, self.S2_pin]
        self._init_pins()
        self.is_running = 0
        self.stop_event = None
        self.experiment: DataFrame = None
        self.total_duration = 0
        self.start_time = None

    @property
    def experiment(self):
        """
        Getter for the experiment variable.
        The experiment variable is a table (DataFrame) with two columns: mode and duration
        """
        return self.__experiment

    @experiment.setter
    def experiment(self, value):
        """
        Setter for the experiment. There is a check to avoid changing the experiment while running.
        """
        if self.is_running:
            print('Unable to overwrite the experiment, stop and then set new experiment')
        else:
            self.__experiment = value

    def run_experiment(self):
        """
        Method that executes the instruction in the experiment (both manual and from file).
        The method checks that an experiment is set. A variable (is_running), which indicates that
        the experiment is running, is set.
        For each instruction in the experiment a method (set_mode) to execute the instruction in Arduino is called.
        """
        if self.experiment is not None:
            self.start_time = datetime.datetime.now()
            self.is_running = True
            self.total_duration = sum(self.experiment['duration'])

            for mode, duration in zip(self.experiment['mode'], self.experiment['duration']):
                print('Running', mode, duration)
                self.set_mode(Modes[mode.title()], duration)
                if self.stop_event.is_set():
                    self.is_running = False
                    break

            self.is_running = False
        print('completed')

    def set_mode(self, mode: Modes, duration):
        """
        Given a mode and a duration, activates the pin on Arduino specific to the mode passed as input.
        """
        # Checks if the mode is valid
        if mode not in Modes:
            print(f"Invalid mode: {mode}")
            return
        # Checks if the duration is valid
        if duration <= 0:
            print(f"Invalid duration: {duration}")
            return
        # Gets the pin values for the selected mode
        valves = mode.value
        # Activates the corresponding pins for the selected mode
        for i, valve in enumerate(self.PINS):
            valve.mode = pyfirmata.OUTPUT
            valve.write(valves[i])
        # Waits for the specified duration
        self.stop_event.wait(duration)  # equivalent to time.sleep but able to be stopped when the stop_event is set.
        # Deactivates all pins
        for pin in self.PINS:
            pin.write(CLOSE)

    def _init_pins(self):
        """
        Initializes the pins on the board by closing them. At the beginning, all valves are closed which is also
        visible in the circle feedback, to prevent a possible leakage.
        """
        for pin in self.PINS:
            pin.mode = pyfirmata.OUTPUT
            pin.write(CLOSE)

    def get_status(self):
        """
        Creates a list in which the boolean status of the pin is read and added.
        """
        status = []
        for pin in self.PINS:
            status.append(pin.read())   # Reads the status of the pin, and saves the value in the status list

        return status