import time

import pyfirmata


class Olfactometer:
    def __init__(self, port):
        self.port = port
        #board = pyfirmata.Arduino(port)
        print(port)

    def print(self, text):
        print('In the Model. Receiving ', text)

    def activate_odor(self, odor_number):
        print(f'Odor {odor_number} activated')

        time.sleep(10)

    def activate_purging(self):
        print('Purging activated')

        time.sleep(10)

    def activate_resting(self):
        print('Resting activated')

        time.sleep(10)

