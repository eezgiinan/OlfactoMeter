import threading
import tkinter as tk
from tkinter import ttk, filedialog

from controller import Controller


def donothing():
    x = 0


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller: Controller = None
        # creates label for box
        self.label = ttk.Label(self, text='Duration:')
        self.label.grid(row=1, column=0)

        # creates a text box and saves the value of the box in duration_var
        self.duration_var = tk.StringVar()
        self.duration_box = ttk.Entry(self, textvariable=self.duration_var, width=30)
        self.duration_box.grid(row=1, column=1, sticky=tk.NSEW)

        # creates a button with a label Print on it. When clicked invokes the method print_button_clicked
        self.print_button = ttk.Button(self, text='Print', command=self.print_button_clicked)
        self.print_button.grid(row=1, column=2, padx=10)

        # creates label for odor box
        self.label = ttk.Label(self, text='Odor:')
        self.label.grid(row=2, column=0)

        # creates a text box and saves the number of odor in odor_num_var
        self.odor_num_var = tk.StringVar()
        self.odor_num_box = ttk.Entry(self, textvariable=self.odor_num_var, width=30)
        self.odor_num_box.grid(row=2, column=1, sticky=tk.NSEW)

        # creates a button for odor
        self.odor_button = ttk.Button(self, text='Odor', command=self.odor_button_clicked)
        self.odor_button.grid(row=2, column=2, padx=10)
        # set the disabled flag
        # self.odor_button.state(['disabled'])

        # creates a button for purging
        self.purging_button = ttk.Button(self, text='Purging', command=self.purging_button_clicked)
        self.purging_button.grid(row=3, column=2, padx=10)

        # creates a button for resting
        self.resting_button = ttk.Button(self, text='Resting', command=self.resting_button_clicked)
        self.resting_button.grid(row=4, column=2, padx=10)

        # creates a button for stop
        self.resting_button = tk.Button(self, text='Purge and Stop', fg='red', command=self.purge_stop_clicked)
        self.resting_button.grid(row=5, column=1, padx=10)

        # creates a button for adding an Excel file
        self.resting_button = tk.Button(self, text='Add file', fg='green', command=self.add_file_clicked)
        self.resting_button.grid(row=7, column=1, padx=10)

        # adds the menu
        self.bar = self.menubar()
        parent.config(menu=self.bar)

        # Creates buttons for valves for displaying state (red is closed and green is open
        self.SA = tk.Button(self, text='SA valve', fg='red')
        self.SA.grid(row=8, column=1, padx=10)
        self.SB = tk.Button(self, text='SB valve', fg='red')
        self.SB.grid(row=8, column=2, padx=10)
        self.S1 = tk.Button(self, text='S1 valve', fg='red')
        self.S1.grid(row=9, column=2, padx=10)
        self.S2 = tk.Button(self, text='S2 valve', fg='red')
        self.S2.grid(row=10, column=2, padx=10)

    def odor_button_clicked(self):
        print('Activating odor', self.odor_num_var.get())
        # Create a new thread (executing unit that can be run in parallel). This in required as the python
        # code can only execute 1 part of the code at a time. Either the UI, or the long-running method we call
        thread = threading.Thread(target=self.controller.activate_odor, args=(self.odor_num_var.get(),))
        thread.start()
        if self.odor_num_var==1:
            self.SA = tk.Button(self, text='SA valve', fg='green')
            self.SA.grid(row=8, column=1, padx=10)
            self.SB = tk.Button(self, text='SB valve', fg='red')
            self.SB.grid(row=8, column=2, padx=10)
            self.S1 = tk.Button(self, text='S1 valve', fg='green')
            self.S1.grid(row=9, column=2, padx=10)
            self.S2 = tk.Button(self, text='S2 valve', fg='red')
            self.S2.grid(row=10, column=2, padx=10)
        else:
            self.SA = tk.Button(self, text='SA valve', fg='green')
            self.SA.grid(row=8, column=1, padx=10)
            self.SB = tk.Button(self, text='SB valve', fg='red')
            self.SB.grid(row=8, column=2, padx=10)
            self.S1 = tk.Button(self, text='S1 valve', fg='red')
            self.S1.grid(row=9, column=2, padx=10)
            self.S2 = tk.Button(self, text='S2 valve', fg='green')
            self.S2.grid(row=10, column=2, padx=10)



    def purging_button_clicked(self):
        print('Activating purging')
        # Create a new thread (executing unit that can be run in parallel). This in required as the python
        # code can only execute 1 part of the code at a time. Either the UI, or the long-running method we call
        thread = threading.Thread(target=self.controller.activate_purge)
        thread.start()
        self.SA = tk.Button(self, text='SA valve', fg='green')
        self.SA.grid(row=8, column=1, padx=10)
        self.SB = tk.Button(self, text='SB valve', fg='green')
        self.SB.grid(row=8, column=2, padx=10)
        self.S1 = tk.Button(self, text='S1 valve', fg='red')
        self.S1.grid(row=9, column=2, padx=10)
        self.S2 = tk.Button(self, text='S2 valve', fg='red')
        self.S2.grid(row=10, column=2, padx=10)


    def resting_button_clicked(self):
        print('Activating resting')
        # Create a new thread (executing unit that can be run in parallel). This in required as the python
        # code can only execute 1 part of the code at a time. Either the UI, or the long-running method we call
        thread = threading.Thread(target=self.controller.activate_rest)
        thread.start()
        self.SA = tk.Button(self, text='SA valve', fg='red')
        self.SA.grid(row=8, column=1, padx=10)
        self.SB = tk.Button(self, text='SB valve', fg='red')
        self.SB.grid(row=8, column=2, padx=10)
        self.S1 = tk.Button(self, text='S1 valve', fg='red')
        self.S1.grid(row=9, column=2, padx=10)
        self.S2 = tk.Button(self, text='S2 valve', fg='red')
        self.S2.grid(row=10, column=2, padx=10)

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

    def print_button_clicked(self):
        print('In the View. Sending', self.duration_var.get())
        self.controller.print(self.duration_var.get())

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


