import tkinter as tk
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

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

    def odor_button_clicked(self):
        print('Activating odor', self.odor_num_var.get())
        self.controller.activate_odor(self.odor_num_var.get())

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
