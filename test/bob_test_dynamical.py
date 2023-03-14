import matplotlib.pyplot as plt
from collections import deque
import random

# MAX NO. OF POINTS TO STORE
que = deque(maxlen=40)

while True:
    # GENERATING THE POINTS - FOR DEMO
    perc = random.random()
    que.append(perc)

    # PLOTTING THE POINTS
    plt.plot(que)
    plt.scatter(range(len(que)), que)

    # SET Y AXIS RANGE
    plt.ylim(-1, 4)

    # DRAW, PAUSE AND CLEAR
    plt.draw()
    plt.pause(0.1)
    plt.clf()

