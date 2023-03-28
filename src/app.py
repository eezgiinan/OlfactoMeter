import tkinter as tk

from controller import Controller
from model import Olfactometer
from view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')
        #self.PORT = 'COM4'
        self.PORT = '/dev/cu.usbmodem1101'
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
