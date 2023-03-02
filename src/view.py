import tkinter as tk
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

        #creates label for box
        self.label = ttk.Label(self, text='Duration:')
        self.label.grid(row=1, column=0)

        # creates a text box and saves the value of the box in duration_var
        self.duration_var = tk.StringVar()
        self.duration_entry = ttk.Entry(self, textvariable=self.duration_var, width=30)
        self.duration_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # creates a button with a label Print on it. When clicked invokes the method print_button_clicked
        self.print_button = ttk.Button(self, text='Print', command=self.print_button_clicked)
        self.print_button.grid(row=1, column=2, padx=10)

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
