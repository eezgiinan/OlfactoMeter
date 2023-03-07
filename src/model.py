import time

import pyfirmata
from pandas import DataFrame


class Olfactometer:
    def __init__(self, port):
        self.port = port
        # board = pyfirmata.Arduino(port)
        print(port)
        self.experiment = None

        # To register the input from duration widget
        self.duration = '0'

        # Countdown Time Left
        self.time_left = 0

        # Is the countdown ongoing ?
        self.ongoing_countdown = False

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

    def print(self, text):
        print('In the Model. Receiving ', text)

    def activate_odor(self, odor_number):
        print(f'Odor {odor_number} activated')

        time.sleep(10)
        print('IT WORKS!')

    def activate_purging(self):
        print('Purging activated')

        time.sleep(10)

    def activate_resting(self):
        print('Resting activated')

        time.sleep(10)

    def activate_stop(self):
        print('Experiment stopped')
        time.sleep(10)


    def run_experiment(self):
        if self.experiment:
            for mode, duration in zip(self.experiment['mode'], self.experiment['duration']):
                print('Running', mode, duration)
                time.sleep(duration)

        print('completed')
