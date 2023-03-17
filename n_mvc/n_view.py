import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time

from n_controller import Controller
from n_modes import Modes


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller: Controller = None

    def set_controller(self, controller):
        """
        Sets the controller
        """
        self.controller = controller
