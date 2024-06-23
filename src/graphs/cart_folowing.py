import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# import matplotlib.pyplot as plt
# import numpy.random as rand
# import pylab

from data.dto import BackRuntime
from backend.init_objects import init_objects

# dt: int
# fig, ax = plt.subplots()
# [line] = ax.step(x, y)

# back_runtime: BackRuntime = init_objects()

# def data_gen():
#     while True:
#         yield 


# def _setting_graph():
#     pylab.minorticks_on()
#     pylab.grid(which="major")
#     pylab.grid(which="minor", linestyle=":")
#     pylab.tight_layout()


# def iter():
#     back_runtime.car.update()
    # for ai_car in back_runtime.car_ai_list:
    #         ai_car.update()
    
    

    

import random
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

back_runtime: BackRuntime = init_objects()

npoints = 60
x = deque([0], maxlen=npoints)
y = deque([0], maxlen=npoints)
fig, ax = plt.subplots()
plt.xlabel("t c")
plt.ylabel("mean_dist м")
plt.title("Средняя диставнция между участниками дорожного потока")
[line] = ax.step(y, x)
i  = 0

def update(dy):
    global i
    if i < 10:
        back_runtime.car.accelerate_x(2.0)
        i += 1
    
    back_runtime.car.update()
    for ai_car in back_runtime.car_ai_list:
            ai_car.update()
    
    a = [car_ai.distance_x for car_ai in back_runtime.car_ai_list]
    m_a = sum(a) / len(a)
    
    x.append(m_a)  
    y.append(y[-1] + dy)

    line.set_xdata(y)  
    line.set_ydata(x)

    ax.relim()  # update axes limits
    ax.autoscale_view(True, True, True)
    return line, ax


def data_gen():
    while True:
        yield 1


ani = animation.FuncAnimation(fig, update, frames=45 ,interval=0.5)
ani.save('car_following_distance.gif', dpi=120, writer='imagemagick')