import threading
import tkinter as tk
from tkinter import ttk, filedialog
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

        """
        # creates a text box and saves the mode in mode_var.
        Keeping it here in case we cannot solve the drop-down box issue
        self.mode_var = tk.StringVar()
        self.mode_box = ttk.Entry(self, textvariable=self.mode_var, width=30)
        self.mode_box.grid(row=2, column=1, sticky=tk.NSEW)
        
        # creates a button for stop
        self.stop_button = tk.Button(self, text='Purge and Stop', fg='red', command=self.purge_stop_clicked)
        self.stop_button.grid(row=7, column=2, padx=10)
        
        # creates a button for adding an Excel file
        self.file_button = tk.Button(self, text='Add file', fg='green', command=self.add_file_clicked)
        self.file_button.grid(row=7, column=1, padx=10)
        """

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

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=5, column=1, sticky=tk.W)

        # Creates colored circles
        self.canvas = tk.Canvas(self, width=100, height=250)
        self.canvas.grid(row=17, column=2, padx=10)

        """
        # Draw 4 circles
        self.circle1 = self.canvas.create_oval(25, 25, 65, 65, fill='red')
        self.circle2 = self.canvas.create_oval(25, 75, 65, 115, fill='red')
        self.circle3 = self.canvas.create_oval(25, 125, 65, 165, fill='red')
        self.circle4 = self.canvas.create_oval(25, 175, 65, 215, fill='red')
        """

        # draw an Oval in the canvas
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

    # reads mode and duration values in the text box and activates a thread that executes them
    def drop_down_click(self):
        print('Activating drop down', self.drop_var.get())
        thread = threading.Thread(target=self.controller.activate_mode_new, args=(self.drop_var.get(), self.duration_var.get(), ))
        thread.start()
        self.status_update()

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

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def menubar(self):
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
        Show an error message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        """
        Hide the message
        :return:
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
        thread = threading.Thread(target=self.controller.run_experiment)
        thread.start()
        self.status_update()

    """
    def change_color(self):
        thread = threading.Thread(target=self.controller.change_color,  args=(self.mode.get(), ))
        thread.start()
    """

    def status_update(self):
        is_running, pins_status = self.controller.get_status()
        # is_running: Whether we are currently executing an experiment (binary) or not
        # pins_status: List of binary values indicating the state of each pin on the board (Open or Closed) eg [1,0,0,1]
        print('Running', is_running)
        print('Status', pins_status)
        for i in range(len(pins_status)):
            self.canvas.itemconfig(self.ovals[i], fill=self.color_map[pins_status[i]]) # ovals corresponding to the pins

        if is_running:
            self.after(1000, self.status_update)
        else:
            print('Completed')

""" 
function to use for connecting pins to ovals

    def run_command(self)
        mode = # read mode from dialog
        status = Modes[mode].value
        for st, canv in zip(sta, canva)
            canv.color(red-green)
"""
