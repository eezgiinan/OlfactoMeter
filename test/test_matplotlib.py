from tkinter import *
from random import randint
import csv

# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading

continuePlotting = False

modes = ["resting", "purging", "odor1", "odor2"]


def change_state():
    global continuePlotting
    if continuePlotting is True:
        continuePlotting = False
    else:
        continuePlotting = True


def data_points():
    f = open("data.txt", "a")
    f.write(str(randint(0, 3)) + '\n')
    f.close()

    f = open("data.txt", "r")
    data = f.readlines()
    f.close()

    plotting_data = []
    for i in range(len(data)):
        plotting_data.append(int(data[i].rstrip("\n")))
    return plotting_data

def app():
    # initialise a window.
    root = Tk()
    root.config(background='white')
    root.geometry("1000x700")

    lab = Label(root, text="Live Plotting", bg='white')
    lab.pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            my_data = data_points()
            ax.plot(my_data[-6:-1], color='orange')
            ax.set_xbound(0, 5)
            ax.set_ybound(-0.5, 3.5)
            ax.set_yticks([0, 1, 2, 3], labels=["Resting", "Purging", "Odor1", "Odor2"])
            graph.draw()
            time.sleep(1)

    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()

    root.mainloop()


if __name__ == '__main__':
    f = open("data.txt", "w")
    f.close()
    app()
