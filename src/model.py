import time

import pyfirmata
from pandas import DataFrame


class Olfactometer:
    def __init__(self, port):
        self.port = port
        #board = pyfirmata.Arduino(port)
        print(port)
        self._experiment = None

    @property
    def experiment(self):
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment

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
