import time
import pyfirmata
from my_modes import *
from olfactometer_machine import *


class Olfactometer:
    def __init__(self, port):
        self.port = port

        """
        self.board = pyfirmata.Arduino(port)
        print(port)
        self.SA_pin = self.board.get_pin('d:4:o')
        self.SB_pin = self.board.get_pin('d:5:o')
        self.S1_pin = self.board.get_pin('d:6:o')
        self.S2_pin = self.board.get_pin('d:7:o')
        self.PINS = [self.SA_pin, self.SB_pin, self.S1_pin, self.S2_pin]
        

        self._init_pins()
        """
        self.experiment = None

        # To register the input from duration widget
        self.duration = '0'

        # Countdown Time Left
        self.time_left = 0

        # Is the countdown ongoing ?
        self.ongoing_countdown = False
        self.experiment = None

        # To register the input from duration widget
        self.duration = '0'

        # Countdown Time Left
        self.time_left = 0

        self.odor_machine = OlfactometerMachine()

    @property
    def experiment(self):
        return self.__experiment

    @experiment.setter
    def experiment(self, value):
        self.__experiment = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if value.isdigit():
            self.__duration = int(value)
        else:
            raise ValueError(f'Invalid duration {value}')

    @property
    def time_left(self):
        return self.__time_left

    @time_left.setter
    def time_left(self, value):
        self.__time_left = value

    @property
    def ongoing_countdown(self):
        return self.__ongoing_countdown

    @ongoing_countdown.setter
    def ongoing_countdown(self, value):
        self.__ongoing_countdown = value

    def time_update(self):
        if self.ongoing_countdown is True:
            if self.time_left == 0:
                self.ongoing_countdown = False
            else:
                self.time_left -= 1

    def run_experiment(self):
        if self.experiment is not None:
            for mode, duration in zip(self.experiment['mode'], self.experiment['duration']):
                print('Running', mode, duration)
                self.set_mode(Modes[mode.title()], duration)
                # time.sleep(duration)

        print('completed')

    """
    # Given a mode and a duration, activates the pin on Arduino specific to the mode passed as input
    def set_mode(self, mode: Modes, duration):
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
        for i, valve in enumerate(self.PINS):
            valve.mode = pyfirmata.OUTPUT
            valve.write(valves[i])
        # Wait for the specified duration
        time.sleep(duration)
        # Deactivate all pins
        for pin in self.PINS:
            pin.write(CLOSE)

    def _init_pins(self):
        for pin in self.PINS:
            pin.mode = pyfirmata.OUTPUT
            pin.write(CLOSE)
    """

    def change_color(self, mode):
        if mode == 'resting':
            self.canvas.itemconfig(self.circle1, fill='red')
            self.canvas.itemconfig(self.circle2, fill='red')
            self.canvas.itemconfig(self.circle3, fill='red')
            self.canvas.itemconfig(self.circle4, fill='red')
        elif mode == 'purging':
            self.canvas.itemconfig(self.circle1, fill='green')
            self.canvas.itemconfig(self.circle2, fill='green')
            self.canvas.itemconfig(self.circle3, fill='red')
            self.canvas.itemconfig(self.circle4, fill='red')
        elif mode == 'odor_1':
            self.canvas.itemconfig(self.circle1, fill='green')
            self.canvas.itemconfig(self.circle2, fill='red')
            self.canvas.itemconfig(self.circle3, fill='green')
            self.canvas.itemconfig(self.circle4, fill='red')
        elif mode == 'odor_2':
            self.canvas.itemconfig(self.circle1, fill='green')
            self.canvas.itemconfig(self.circle2, fill='red')
            self.canvas.itemconfig(self.circle3, fill='red')
            self.canvas.itemconfig(self.circle4, fill='green')