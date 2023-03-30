import tkinter as tk
from controller import Controller
from model import Olfactometer
from view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Olfactometer')
        self.PORT = 'COM3'
        # self.PORT = '/dev/cu.usbmodem1101' was used as an input for Mac.
        # creates a model
        model = Olfactometer(self.PORT)

        # creates a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # creates a controller
        controller = Controller(model, view)

        # sets the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
