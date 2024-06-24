import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data.dto import BackRuntime
from backend.init_objects import init_objects

from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# back_runtime: BackRuntime = init_objects()

# npoints = 60
# x = deque([0], maxlen=npoints)
# y = deque([0], maxlen=npoints)
# fig, ax = plt.subplots()
# plt.xlabel("t c")
# plt.ylabel("mean_dist м")
# plt.title("Средняя диставнция между участниками дорожного потока")
# [line] = ax.step(y, x)
# i  = 0

# def update(dy):
#     global i
#     if i < 10:
#         back_runtime.car.accelerate_x(2.0)
#         i += 1

#     back_runtime.car.update()
#     for ai_car in back_runtime.car_ai_list:
#             ai_car.update()

#     a = [car_ai.distance_x for car_ai in back_runtime.car_ai_list]
#     m_a = sum(a) / len(a)

#     x.append(m_a)
#     y.append(y[-1] + dy)

#     line.set_xdata(y)
#     line.set_ydata(x)

#     ax.relim()  # update axes limits
#     ax.autoscale_view(True, True, True)
#     return line, ax


# def data_gen():
#     while True:
#         yield 1


# ani = animation.FuncAnimation(fig, update, frames=100 ,interval=0.5)
# ani.save('car_following_distance.gif', dpi=120, writer='imagemagick')


def run(iterations: int, back_runtime: BackRuntime):
    i_accel: int = int(iterations * 0.1)
    for i in range(iterations):
        if i < i_accel:
            back_runtime.car.accelerate_x(2.0)
        back_runtime.car.update()
        for ai_car in back_runtime.car_ai_list:
            ai_car.update()

        yield back_runtime


def _setting_graph():
    plt.minorticks_on()
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":")
    plt.tight_layout()


def main():
    iteration = 1000
    back_runtime: BackRuntime = init_objects()
    iterat = run(iteration, back_runtime)

    x = [time for time in range(iteration)]
    y = []
    y_0 = []

    for runtime in iterat:
        dist = [car.distance_x for car in runtime.car_ai_list]
        y.append(sum(dist) / len(dist))
        y_0.append(runtime.car_ai_list[0].distance_x)

    plt.plot(x, y, label="Средняя дистанция")  # , alpha=0.8)
    plt.plot(x, y_0, label="Дистанция 1ого за лидером")  # , alpha=0.8)
    plt.title("Дистанция")
    plt.xlabel("t, c")
    plt.ylabel("d, м")
    plt.legend(loc="upper left")

    _setting_graph()
    plt.show()


main()
