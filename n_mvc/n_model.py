import time
from threading import Event

import pyfirmata
from pandas import DataFrame
from n_modes import *


class Olfactometer:
    def __init__(self, port):
        self.not_sed = 0
