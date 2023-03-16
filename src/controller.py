import pandas as pd

from model import Olfactometer
from modes import Modes


class Controller:
    def __init__(self, model: Olfactometer, view):
        self.model: Olfactometer = model
        self.view = view

    def activate_mode(self, mode, duration, event):
        """
        Creates an experiment (DataFrame) from the mode and duration given as an input from the UI.
        Sets the experiment in the model and runs it.
        """
        experiment = pd.DataFrame([(mode, int(duration))], columns=['mode', 'duration'])
        # We call the setter. This is how it would look like in Java: this.model.set_experiment(experiment).
        self.model.experiment = experiment
        self.run_experiment(event)

    def experiment_from_file(self, filename: str):
        """
        Reads an experiment file (.csv or .xlsx) as a DataFrame and saves it in the model.
        """
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

    def run_experiment(self, event):
        """
        Checks if the model is running, if it doesn't it runs the experiment.
        """
        if not self.model.is_running:
            self.model.stop_event = event
            self.model.run_experiment()
        else:
            self.view.show_warn('Ongoing experiment', 'Unable to run, already running! Stop and purge before running again')

    def get_status(self):
        """
        Returns the status of the model.
        """
        return self.model.is_running, self.model.get_status()

    def clean(self):
        """
        After stopping activates purging in the model
        """
        self.model.set_mode(Modes.Purging, 10)

