import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import time
import matplotlib
import csv
import pandas as pd
import numpy as np
from controller import Controller
from modes import Modes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from time import strftime


def donothing():
    x = 0


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller: Controller = None

        # creates frame
        self.frame1 = tk.Frame(self, width=200, height=200, bg='#DDA0DD', borderwidth=2, relief="ridge")
        self.frame1.grid(row=1, column=1, sticky="sew", padx=3, pady=3)

        self.frame2 = tk.Frame(self, width=200, height=200, bg='#E6E6FA', borderwidth=2, relief="ridge")
        self.frame2.grid(row=2, column=1, sticky="new", padx=3, pady=3)

        self.frame3 = tk.Frame(self, width=200, height=200, bg='#FFC0CB', borderwidth=2, relief="ridge")
        self.frame3.grid(row=2, column=1, sticky="ew", padx=3, pady=3)

        self.frame4 = tk.Frame(self, width=300, height=600, bg='#B2DF9B', borderwidth=2, relief="ridge")
        self.frame4.grid(row=2, column=2, sticky="new", padx=3, pady=3)

        self.frame5 = tk.Frame(self, width=300, height=600, bg='#B0E0E6', borderwidth=2, relief="ridge")
        self.frame5.grid(row=1, column=2, sticky="new", padx=3, pady=3)

        self.frame6 = tk.Frame(self, width=200, height=600, bg='#B2DF9B', borderwidth=2, relief="ridge")
        self.frame6.grid(row=3, column=2, sticky="n", padx=3, pady=3)

        # creates title for frame1
        self.title_frame1 = tk.Label(self.frame1, text='Manual control', bg='#DDA0DD', font=("Arial bold", 16))
        self.title_frame1.grid(row=0, sticky="ew")

        # creates title for frame2
        self.title_frame2 = tk.Label(self.frame2, text='Excel control', bg='#E6E6FA', font=("Arial bold", 16))
        self.title_frame2.grid(row=0, sticky="ew")

        # creates title for frame3
        self.title_frame3 = tk.Label(self.frame3, text='STOP', bg='#FFC0CB', font=("Arial bold", 16))
        self.title_frame3.grid(row=0, sticky="ew")

        # creates title for frame4
        self.title_frame4 = tk.Label(self.frame4, text='Feedback', bg='#B2DF9B', font=("Arial bold", 16))
        self.title_frame4.grid(row=0, sticky="ew")

        # creates title for frame5
        self.title_frame5 = tk.Label(self.frame5, text='Experiment Information', bg='#B0E0E6', font=("Arial bold", 16))
        self.title_frame5.grid(row=0, sticky="ew")

        # creates title for frame6
        self.title_frame6 = tk.Label(self.frame6, text='Plot Feedback', bg='#B2DF9B', font=("Arial bold", 16))
        self.title_frame6.grid(row=0, sticky="ew")

        # creates label for box
        self.select_duration = tk.Label(self.frame1, text='Select the duration:', bg='#DDA0DD')
        self.select_duration.grid(row=3, column=0)

        # creates a text box and saves the value of the box in duration_var
        self.duration_var = tk.StringVar()
        self.duration_box = ttk.Entry(self.frame1, textvariable=self.duration_var, width=30)
        self.duration_box.grid(row=3, column=1)

        # creates label for mode box
        self.mode = tk.Label(self.frame1, text='Select the mode:', bg='#DDA0DD')
        self.mode.grid(row=2, column=0, padx=10)

        # Run Experiment button
        self.run_exp_button = ttk.Button(self.frame2, text='Run file', command=self.run_file)
        self.run_exp_button.grid(row=3, column=1, padx=10)

        # Event thread for the stop button
        self.stop_event = threading.Event()

        # drop down menu for mode selection
        self.drop_var = tk.StringVar()
        self.drop = ttk.Combobox(self.frame1, state="readonly", textvariable=self.drop_var,
                                 values=[mode.name for mode in Modes])
        self.drop.grid(row=2, column=1, padx=10)

        # drop down button
        self.drop_button = ttk.Button(self.frame1, text='Run', command=self.run_manual)
        self.drop_button.grid(row=4, column=1, padx=10)
        self.drop_button = ttk.Button(self.frame1, text='Reset history', command=self.manual_file)
        self.drop_button.grid(row=4, column=0, padx=10)

        # creates a button for stop
        self.stop_button = tk.Button(self.frame3, text='Purge and Stop', fg='red', command=self.stop_experiment)
        self.stop_button.grid(row=2, column=1, padx=10)

        # Creates colored circles
        self.canvas = tk.Canvas(self.frame4, width=210, height=140)
        self.canvas.grid(row=1, column=0, padx=10)

        # progress bar
        self.pb = ttk.Progressbar(self.frame4, orient='horizontal', mode='determinate', length=200)
        self.pb.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # progress bar label
        self.pb_label = tk.Label(self.frame4, bg='#B2DF9B', font=("Arial bold", 13))
        self.pb_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        # selected file label
        self.file_label = ttk.Label(self.frame2, text='Please choose a file')
        self.file_label.grid(row=4, column=1)

        # draw an oval in the canvas
        self.ovals = [self.canvas.create_oval(25, 25, 65, 65), self.canvas.create_oval(25, 75, 65, 115),
                      self.canvas.create_oval(85, 25, 125, 65), self.canvas.create_oval(145, 25, 185, 65)]
        for oval in self.ovals:
            self.canvas.itemconfig(oval, fill="yellow")

        # create the labels for the ovals
        self.label1 = self.canvas.create_text(20, 10, text="SA valve", anchor='nw', fill="black")
        self.label2 = self.canvas.create_text(20, 115, text="SB valve", anchor='nw', fill="black")
        self.label3 = self.canvas.create_text(80, 10, text="S1 valve", anchor='nw', fill="black")
        self.label4 = self.canvas.create_text(140, 10, text="S2 valve", anchor='nw', fill="black")

        # create assignment to status
        self.color_map = {0: 'green', 1: 'red'}

        # creates label for the odors name
        self.mode_odor1 = tk.Label(self.frame5, text='Odor 1 :', bg='#B0E0E6')
        self.mode_odor1.grid(row=2, column=0)
        self.mode_odor2 = tk.Label(self.frame5, text='Odor 2 :', bg='#B0E0E6')
        self.mode_odor2.grid(row=3, column=0)

        # creates a text box for odors name and saves the name in odor_name
        self.odor1_name = tk.StringVar(value='Odor 1')
        self.odor1_box = ttk.Entry(self.frame5, textvariable=self.odor1_name, width=30)
        self.odor1_box.grid(row=2, column=1)
        self.odor2_name = tk.StringVar(value='Odor 2')
        self.odor2_box = ttk.Entry(self.frame5, textvariable=self.odor2_name, width=30)
        self.odor2_box.grid(row=3, column=1)

        # creates label for mouse number
        self.mode_mouse = tk.Label(self.frame5, text='Mouse n°:', bg='#B0E0E6')
        self.mode_mouse.grid(row=4, column=0)
        # creates a text box for mouse number and saves the name in mouse_nb
        self.mouse_nb = tk.StringVar(value='mouse_unknown')
        self.mouse_box = ttk.Entry(self.frame5, textvariable=self.mouse_nb, width=30)
        self.mouse_box.grid(row=4, column=1)

        # creates label for protocol used
        self.mode_protocol = tk.Label(self.frame5, text='Protocol used : ', bg='#B0E0E6')
        self.mode_protocol.grid(row=5, column=0)

        # creates a text box for protocol used and saves the name in protocol
        self.protocol = tk.StringVar(value='unknown_protocol')
        self.protocol_box = ttk.Entry(self.frame5, textvariable=self.protocol, width=30)
        self.protocol_box.grid(row=5, column=1)

        # creates a button for saving
        self.file_button_save = ttk.Button(self.frame5, text='Save', command=self.save_names)
        self.file_button_save.grid(row=6, column=1)

        # creates a button for using a previous setup
        self.file_button_setup = ttk.Button(self.frame5, text='Previous Setup', command=self.browse_setup)
        self.file_button_setup.grid(row=6, column=0)

        # creates a button for adding an Excel file
        self.file_button_add = ttk.Button(self.frame2, text='Add file', command=self.browse_files)
        self.file_button_add.grid(row=2, column=1, padx=10)

        self.fig = plt.figure(figsize=(6, 2), dpi=100)
        self.experiment_labels = ['Resting', 'Purging', self.odor1_name.get(), self.odor2_name.get()]
        self.ax = plt.axes(ylim=(-0.5, 3.5))
        self.ax.set_yticks(np.arange(0, len(self.experiment_labels)), labels=self.experiment_labels)

        # specify the window as master
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.frame6)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().grid(row=1, column=0, ipadx=3, ipady=3)

        self.history_file = None
        self.manual_file = None

        # Create another canva for explanation of the valves
        self.canvas2 = tk.Canvas(self.frame4, width=160, height=140)
        self.canvas2.grid(row=1, column=1, padx=10)
        # draw ovals in the canvas
        self.ovals2 = [self.canvas2.create_oval(25, 25, 65, 65), self.canvas2.create_oval(25, 75, 65, 115)]
        for oval in self.ovals2:
            self.canvas2.itemconfig(oval, fill="green")

        # create the labels for the ovals
        self.labels = self.canvas2.create_text(20, 10, text="SA valve", anchor='nw', fill="black")
        self.labels = self.canvas2.create_text(20, 115, text="SB valve", anchor='nw', fill="black")
        self.labels = self.canvas2.create_text(80, 60, font=('freemono', 12, 'bold'), text="Purging", anchor='nw',
                                               fill="black")

        # Create another canva for explanation of the valves
        self.canvas3 = tk.Canvas(self.frame4, width=160, height=140)
        self.canvas3.grid(row=1, column=2, padx=10)
        # draw ovals in the canvas
        self.ovals3 = [self.canvas3.create_oval(25, 25, 65, 65), self.canvas3.create_oval(85, 25, 125, 65)]
        for oval in self.ovals3:
            self.canvas3.itemconfig(oval, fill="green")

        # create the labels for the ovals
        self.labels = self.canvas3.create_text(20, 10, text="SA valve", anchor='nw', fill="black")
        self.labels = self.canvas3.create_text(80, 10, text="S1 valve", anchor='nw', fill="black")
        self.labels = self.canvas3.create_text(60, 80, font=('freemono', 12, 'bold'), text="Odor 1", anchor='nw',
                                               fill="black")

        # Create another canva for explanation of the valves
        self.canvas4 = tk.Canvas(self.frame4, width=160, height=140)
        self.canvas4.grid(row=1, column=3, padx=10)
        # draw ovals in the canvas
        self.ovals4 = [self.canvas4.create_oval(25, 25, 65, 65), self.canvas4.create_oval(85, 25, 125, 65)]
        for oval in self.ovals4:
            self.canvas4.itemconfig(oval, fill="green")

        # create the labels for the ovals
        self.labels = self.canvas4.create_text(20, 10, text="SA valve", anchor='nw', fill="black")
        self.labels = self.canvas4.create_text(80, 10, text="S2 valve", anchor='nw', fill="black")
        self.labels = self.canvas4.create_text(60, 80, font=('freemono', 12, 'bold'), text="Odor 2", anchor='nw',
                                               fill="black")

    def save_names(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        with open(filename, 'w') as file:
            file.write(self.odor1_box.get() + '\n')
            file.write(self.odor2_box.get() + '\n')
            file.write(self.mouse_box.get() + '\n')
            file.write(self.protocol_box.get() + '\n')
        plt.clf()
        self.ax = plt.axes(ylim=(-0.5, 3.5))
        self.ax.set_yticks(np.arange(0, len(self.experiment_labels)),
                           labels=['Resting', 'Purging', self.odor1_box.get(), self.odor2_box.get()])
        self.plot_canvas.draw()

    def browse_setup(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=[("text files",
                                                          "*.txt")])
        plt.clf()
        self.ax = plt.axes(ylim=(-0.5, 3.5))
        with open(filename, 'r') as file:
            lines = [line.rstrip() for line in file]
            self.odor1_name.set(lines[0])
            self.odor2_name.set(lines[1])
            self.mouse_nb.set(lines[2])
            self.protocol.set(lines[3])
            self.ax.set_yticks(np.arange(0, len(self.experiment_labels)),
                               labels=['Resting', 'Purging', lines[0], lines[1]])
        self.plot_canvas.draw()

    def set_controller(self, controller):
        """
        Sets the controller
        """
        self.controller = controller

    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=[("excel files",
                                                          "*.xlsx"),
                                                         ("CSV files",
                                                          "*.csv")
                                                         ])

        # Change label contents
        self.update()
        self.controller.experiment_from_file(filename)
        self.file_label["text"] = Path(filename).name

    def run_manual(self):
        """
        Reads the mode and duration values in the text box and activates a thread that executes them
        """
        print('Activating drop down', self.drop_var.get())
        thread = threading.Thread(target=self.controller.activate_mode,
                                  args=(self.drop_var.get(), self.duration_var.get(), self.stop_event,))
        thread.start()
        self.history_file = self.manual_file
        self.status_update()
        self.file_label["text"] = 'Please choose a file'

    def run_file(self):
        """
        Creates a thread that runs the experiment and calls the status_update method.
        """
        thread = threading.Thread(target=self.controller.run_experiment, args=(self.stop_event,))
        thread.start()
        self.history_file = self.protocol.get() + '__' + strftime("%a-%d-%b-%Y__%H-%M-%S") + '.csv'
        self.init_history_file()
        self.status_update()

    def init_manual_file(self):
        self.manual_file = 'manual' + '__' + self.protocol.get() + '__' + strftime("%a-%d-%b-%Y__%H-%M-%S") + '.csv'
        self.history_file = self.manual_file
        self.init_history_file()

    def init_history_file(self):
        with open(self.history_file, 'w', newline='') as csvfile:
            fieldnames = ['Time', 'State', 'SA', 'SB', 'S1', 'S2']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def stop_experiment(self):
        self.show_warn(title='Stop the experiment',
                       message='Purging will be activated and the experiment will be stopped. Do you wish to proceed?')
        self.stop_event.set()
        time.sleep(1)
        thread = threading.Thread(target=self.controller.clean)
        thread.start()
        self.status_update()
        self.file_label["text"] = 'Please choose a file'

    def show_warn(self, title, message):
        messagebox.askyesnocancel(title=title, message=message)

    def status_update(self):
        """
        Reads the status from controller and assigns them to is_running and pins_status. Then it creates correspondence
        between the created ovals and pins_status using color_map. Then it repeats itself every 1 second using after().
        """

        # is_running: Whether we are currently executing an experiment (binary) or not
        # pins_status: List of binary values indicating the state of each pin on the board (Open or Closed) eg [1,0,0,1]
        is_running, pins_status = self.controller.get_status()
        percent_completed, elapsed, total_duration = self.controller.get_progress()

        self.pb['value'] = percent_completed
        self.pb_label['text'] = f"Elapsed {elapsed} seconds out of {total_duration} seconds"
        for i in range(len(pins_status)):
            self.canvas.itemconfig(self.ovals[i],
                                   fill=self.color_map[pins_status[i]])  # ovals corresponding to the pins

        self.plot_history(elapsed, pins_status)
        if is_running:
            self.after(1000, self.status_update)
        else:
            print('Completed')

    def plot_history(self, elapsed, pins_status):
        state = None
        for mode in Modes:
            if tuple(pins_status) == mode.value:
                state = mode.name

        if not state:
            raise ValueError('Unknown pin status configuration', pins_status)

        with open(self.history_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            row = [elapsed, state] + pins_status
            writer.writerow(row)

        df = pd.read_csv(self.history_file)
        x = df['Time'][-6:].values.tolist()
        y = df['State'][-6:]
        words = [mode.name for mode in Modes]
        y = [words.index(i) for i in y]
        self.experiment_labels = ['Resting', 'Purging', self.odor1_name.get(), self.odor2_name.get()]
        plt.clf()
        self.ax = plt.axes(ylim=(-0.5, 3.5))
        self.ax.set_yticks(np.arange(0, len(self.experiment_labels)), labels=self.experiment_labels)
        print(x, y)
        plt.plot(x, y)
        self.plot_canvas.draw()
