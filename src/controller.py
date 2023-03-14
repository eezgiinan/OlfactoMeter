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

    def activate_mode_new(self, mode, duration):
        experiment = pd.DataFrame([(mode, int(duration))], columns=['mode', 'duration'])
        self.model.experiment = experiment
        self.run_experiment()

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
        if not self.model.is_running:
            self.model.run_experiment()
        else:
            print('Unable to run, already running! Stop and purge before running again')

    def get_status(self):
        return self.model.is_running, self.model.get_status()

