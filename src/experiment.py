import tkinter as tk
import matplotlib
import random
import csv
import time
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from time import strftime


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Matplotlib Demo')
        self.mouse_name = 'unknown_mouse'
        self.filename = self.mouse_name + '__' + strftime("%a-%d-%b-%Y__%H-%M-%S") + '.csv'
        self.start_time = time.time()

        data = {
            'Python': 11.27,
            'C': 11.16,
            'Java': 10.46,
            'C++': 7.5,
            'C#': 5.26
        }
        languages = data.keys()
        popularity = data.values()

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(languages, popularity)
        axes.set_title('Top 5 Programming Languages')
        axes.set_ylabel('Popularity')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ['Time', 'State', 'SA', 'SB', 'S1', 'S2']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        self.after(1, self.update_plot)

        # prepare data
    def get_status(self):
        a = random.randint(0, 4)
        if a == 0:
            return [1, 1, 1, 1]
        elif a == 1:
            return [0, 0, 1, 1]
        elif a == 2:
            return [0, 1, 0, 1]
        else:
            return [0, 1, 1, 0]

    def update_plot(self):
        pins_state = self.get_status()
        timing = int(time.time() - self.start_time)
        if pins_state[0] == 1:
            state = 'resting'
        else:
            if pins_state[1] == 0:
                state = 'purging'
            else:
                if pins_state[2] == 0:
                    state = 'odor_1'
                else:
                    state = 'odor_2'

        with open(self.filename, 'a', newline='') as csvfile:
            fieldnames = ['Time', 'State', 'SA', 'SB', 'S1', 'S2']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({fieldnames[0]: timing, fieldnames[1]: state, fieldnames[2]: pins_state[0],
                             fieldnames[3]: pins_state[1], fieldnames[4]: pins_state[2], fieldnames[5]: pins_state[3]})

        self.after(1000, self.update_plot)


if __name__ == '__main__':
    app = App()
    app.mainloop()
