import tkinter as tk

from my_controller import Controller
from my_model import Olfactometer
from my_view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')
        self.PORT = 'COM3'
        # self.PORT = '/dev/cu.usbmodem1101'
        # create a model
        model = Olfactometer(self.PORT)

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()