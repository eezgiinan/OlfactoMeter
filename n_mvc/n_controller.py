import pandas as pd
from n_model import Olfactometer
from n_modes import Modes


class Controller:
    def __init__(self, model: Olfactometer, view):
        self.model: Olfactometer = model
        self.view = view
