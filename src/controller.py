import pandas as pd
from modes import Modes
from model import Olfactometer


class Controller:
    def __init__(self, model: Olfactometer, view):
        self.model: Olfactometer = model
        self.view = view

    """
    def print(self, text):
        print('In the controller. Propagating', text)
        self.model.print(text)
    """
# Activates the mode received from the view
    def activate_mode(self, mode, duration):
        mode = Modes[mode.title()]
        duration = int(duration)
        self.model.set_mode(mode, duration)

    def experiment_from_file(self, filename: str):
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filename, engine='openpyxl')
        else:
            raise TypeError('Unsupported File')

        print('Loaded', df.head())
        self.model.experiment = df

    def set_duration(self, duration):
        try:
            self.model.duration = duration
            self.view.show_success(f'Duration set to {duration}s')
            self.model.time_left = int(duration)
            self.model.ongoing_countdown = False
        except ValueError as error:
            self.view.show_error(error)

    def get_time(self):
        return self.model.time_left

    def time_update(self):
        self.model.time_update()

    def start_countdown(self):
        self.model.ongoing_countdown = True

    def run_experiment(self):
        self.model.run_experiment()

    def get_mode(self, mode, duration):
        mode = Modes[mode.title()]
        duration = int(duration)
        self.model.get_mode(mode)
    """
    def run_manual_experiment(self, duration, odor, purging, resting):
        self.view.duration_var = duration
        self.view.mode_var = odor
        self.view.purging_button = purging
        self.view.resting_button = resting
        self.model.run_manual_experiment()
    """
