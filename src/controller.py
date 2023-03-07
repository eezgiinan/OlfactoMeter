import pandas as pd

from model import Olfactometer


class Controller:
    def __init__(self, model: Olfactometer, view):
        self.model: Olfactometer = model
        self.view = view

    def print(self, text):
        print('In the controller. Propogating', text)
        self.model.print(text)

    def activate_odor(self, odor_number):
        self.model.activate_odor(odor_number)

    def activate_purge(self):
        self.model.activate_purging()

    def activate_rest(self):
        self.model.activate_resting()

    def activate_stop(self):
        self.model.activate_stop()

    def experiment_from_file(self, filename: str):
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filename)
        else:
            raise TypeError('Unsupported File')

        print('Loaded', df.head())
        self.model.experiment = df

    def run_experiment(self):
        self.model.run_experiment()
