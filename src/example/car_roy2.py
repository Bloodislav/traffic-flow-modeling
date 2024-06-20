import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import matplotlib.pyplot as plt
import numpy.random as rand
import pylab

from backend.models.roy2 import Roy2
from backend.models.car_agent import CarAgent
from backend.configs.config import setting as back_sett


def _setting_graph():
    pylab.minorticks_on()
    pylab.grid(which="major")
    pylab.grid(which="minor", linestyle=":")
    pylab.tight_layout()


def main2():
    roy: Roy2 = Roy2()
    agents_list: list[list[CarAgent]] = roy.init_agents(back_sett.roy.count_lanes)
    # iterations = roy.run2(agents_list)

    # data for graph
    speed_time: list[int] = [i for i in range(back_sett.roy.iteration)]
    middle_speeds: list[float] = []
    # flow_densities: list[float] = []
    # flow_rates: list[float] = []
    changes_line: list[float] = []

    # data filling
    for agents in roy.run(agents_list):
        # средняя скорость
        speeds: list[float] = [agent[0].velocity for agent in agents] + [
            agent[1].velocity for agent in agents
        ]
        middle_speed: float = float("{:.5f}".format(sum(speeds) / len(speeds)))
        middle_speeds.append(middle_speed)

        # кол-во перестреоний
        count: float = sum([agent[0].changing_line for agent in agents]) + sum(
            [agent[1].changing_line for agent in agents]
        )
        changes_line.append(count)

    # строки - 2, столбца - 3, Текущая ячейка - 3
    pylab.subplot(2, 3, 3)
    pylab.plot(speed_time, middle_speeds, ":b", alpha=0.8)
    pylab.xlabel("t, c")
    pylab.ylabel("v, м/с")
    pylab.ylim([0, max(middle_speeds) + 2])

    # setting graph - 3
    _setting_graph()

    # строки - 2, столбца - 3, Текущая ячейка - 1
    pylab.subplot(2, 3, 1)
    pylab.plot(speed_time, changes_line, ":b", alpha=0.8)
    pylab.xlabel("t, c")
    pylab.ylabel("количество пересроений")
    # pylab.ylim([0, max(middle_speeds) + 2])

    # setting graph - 3
    _setting_graph()

    pylab.show()


if __name__ == "__main__":
    main2()
