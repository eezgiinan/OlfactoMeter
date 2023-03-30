import datetime
import time
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

    def run_experiment(self, event):
        """
        Checks if the model is running, if it doesn't it runs the experiment.
        """
        if not self.model.is_running:
            self.model.stop_event = event
            self.model.run_experiment()
        else:
            self.view.show_warn('Ongoing experiment',
                                'Unable to run, already running! Stop and purge before running again')

    def get_status(self):
        """
        Returns the status of the model.
        """
        return self.model.is_running, self.model.get_status()

    def get_progress(self):
        elapsed = datetime.datetime.now() - self.model.start_time
        percent_completed = elapsed.total_seconds() / self.model.total_duration * 100
        return percent_completed, int(elapsed.total_seconds()), self.model.total_duration

    def clean(self):
        """
        After stopping activates purging in the model
        """
        self.model.is_running = False
        self.model.stop_event.clear()
        experiment = pd.DataFrame([(Modes.Purging.name, 10)], columns=['mode', 'duration'])
        # We call the setter. This is how it would look like in Java: this.model.set_experiment(experiment).
        self.model.experiment = experiment
        self.run_experiment(self.model.stop_event)
        self.view.status_update()
