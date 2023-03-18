import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time

from controller import Controller
from modes import Modes


def donothing():
    x = 0


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller: Controller = None
        # creates label for box
        self.mode = ttk.Label(self, text='Select the duration:')
        self.mode.grid(row=1, column=0)

        # creates a text box and saves the value of the box in duration_var
        self.duration_var = tk.StringVar()
        self.duration_box = ttk.Entry(self, textvariable=self.duration_var, width=30)
        self.duration_box.grid(row=1, column=1)

        # creates label for mode box
        self.mode = ttk.Label(self, text='Select the mode:')
        self.mode.grid(row=2, column=0, padx=10)

        # Run Experiment button
        self.run_exp_button = ttk.Button(self, text='Run file', command=self.run_experiment)
        self.run_exp_button.grid(row=6, column=1, padx=10)

        # Event thread for the stop button
        self.stop_event = threading.Event()

        # adds the menu
        self.bar = self.menubar()
        parent.config(menu=self.bar)

        # drop down menu for mode selection
        self.drop_var = tk.StringVar()
        self.drop = ttk.Combobox(self, state="readonly", textvariable=self.drop_var, values=[mode.name for mode in Modes])
        self.drop.grid(row=2, column=1, padx=10)

        # drop down button
        self.drop_button = ttk.Button(self, text='Run drop down', command=self.drop_down_click)
        self.drop_button.grid(row=8, column=1, padx=10)

        # creates a button for stop
        self.stop_button = tk.Button(self, text='Purge and Stop', fg='red', command=self.stop_experiment)
        self.stop_button.grid(row=7, column=2, padx=10)

        # creates colored circles
        self.canvas = tk.Canvas(self, width=100, height=250)
        self.canvas.grid(row=17, column=2, padx=10)

        # progress bar
        self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.pb.grid(row=1, column=3, columnspan=2)

        # progress bar label
        self.pb_label = ttk.Label(self)
        self.pb_label.grid(row=2, column=3, columnspan=2)

        # draw an oval in the canvas
        self.ovals = [self.canvas.create_oval(25, 25, 65, 65), self.canvas.create_oval(25, 75, 65, 115),
                      self.canvas.create_oval(25, 125, 65, 165), self.canvas.create_oval(25, 175, 65, 215)]
        for oval in self.ovals:
            self.canvas.itemconfig(oval, fill="yellow")

        # create assignment to status
        self.color_map = {0: 'green', 1: 'red'}

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=5, column=1, sticky=tk.W)

        # set duration button
        self.set_duration_button = ttk.Button(self, text='Set Duration', command=self.set_duration)
        self.set_duration_button.grid(row=14, column=2, padx=10)

        # start countdown button
        self.start_countdown_button = ttk.Button(self, text='Start Countdown', command=self.start_countdown)
        self.start_countdown_button.grid(row=15, column=2, padx=10)

        # countdown label
        self.countdown_label = ttk.Label(
            self,
            text=self.time_string(),
            font=('Digital-7', 40),
            background='black',
            foreground='red')

        self.countdown_label.grid(row=15, column=1, padx=10)
        # schedule an update every 1 second
        self.countdown_label.after(1000, self.countdown_update)

    def drop_down_click(self):
        """
        Reads the mode and duration values in the text box and activates a thread that executes them
        """
        print('Activating drop down', self.drop_var.get())
        thread = threading.Thread(target=self.controller.activate_mode, args=(self.drop_var.get(), self.duration_var.get(), self.stop_event, ))
        thread.start()
        self.status_update()

    def set_controller(self, controller):
        """
        Sets the controller
        """
        self.controller = controller

    def menubar(self):
        """
        Creates the menubar for file selection.
        """
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=self.browse_files)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        return menubar

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

    def show_error(self, message):
        """
        Shows an error message
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Shows a success message
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        """
        Hides the message
        """
        self.message_label['text'] = ''

    def set_duration(self):
        if self.controller:
            self.controller.set_duration(self.duration_var.get())
            self.countdown_label.configure(text=self.time_string())

    def time_string(self):
        if self.controller:
            return time.strftime('%M:%S', time.gmtime(self.controller.get_time()))
        else:
            return time.strftime('%M:%S', time.gmtime(0))

    def countdown_update(self):
        if self.controller:
            self.controller.time_update()

        self.countdown_label.configure(text=self.time_string())

        # schedule another timer
        self.countdown_label.after(1000, self.countdown_update)

    def start_countdown(self):
        if self.controller:
            self.controller.start_countdown()

    def run_experiment(self):
        """
        Creates a thread that runs the experiment and calls the status_update method.
        """
        # self.stop_event.clear()
        thread = threading.Thread(target=self.controller.run_experiment, args=(self.stop_event, ))
        thread.start()
        self.status_update()

    def stop_experiment(self):
        self.show_warn(title='Stop the experiment', message='Purging will be activated and the experiment will be stopped. Do you wish to proceed?')
        self.stop_event.set()
        # CLEAR
        thread = threading.Thread(target=self.controller.clean)
        thread.start()
        self.status_update()

    def show_warn(self, title, message):
        messagebox.askyesnocancel(title=title, message=message)

    def status_update(self):
        """
        Reads the status from controller and assigns them to is_running and pins_status. Then it creates correspondence
        between the created ovals and pins_status using color_map. Then it repeats itself every 1 second using after().
        """
        is_running, pins_status, percent_completed, elapsed, total_duration = self.controller.get_status()
        # is_running: Whether we are currently executing an experiment (binary) or not
        # pins_status: List of binary values indicating the state of each pin on the board (Open or Closed) eg [1,0,0,1]
        print('Running', is_running)
        print('Status', pins_status)
        self.pb['value'] = percent_completed
        self.pb_label['text'] = f"Elapsed {elapsed} seconds out of {total_duration} seconds"
        for i in range(len(pins_status)):
            self.canvas.itemconfig(self.ovals[i], fill=self.color_map[pins_status[i]]) # ovals corresponding to the pins

        if is_running:
            self.after(1000, self.status_update)
        else:
            print('Completed')

        """ 
        # creates a button for adding an Excel file
        self.file_button = tk.Button(self, text='Add file', fg='green', command=self.add_file_clicked)
        self.file_button.grid(row=7, column=1, padx=10)
        """

        """
        def purge_stop_clicked(self):
            print('Activating Purge and Stop')
            # Create a new thread (executing unit that can be run in parallel). This in required as the python
            # code can only execute 1 part of the code at a time. Either the UI, or the long-running method we call
            thread = threading.Thread(target=self.controller.activate_stop)
            thread.start()

        def add_file_clicked(self):
            print('Add an Excel file')
            # Create a new thread (executing unit that can be run in parallel). This in required as the python
            # code can only execute 1 part of the code at a time. Either the UI, or the long-running method we call
            thread = threading.Thread(target=self.controller.experiment_from_file)
            thread.start()
        """