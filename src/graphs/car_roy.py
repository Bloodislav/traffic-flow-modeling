import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import matplotlib.pyplot as plt
import numpy.random as rand
import pylab

from backend.models.roy import Roy, CarAgent
from backend.models.roy3 import Roy3
from backend.configs.config import setting as back_sett


def _setting_graph():
    pylab.minorticks_on()
    pylab.grid(which="major")
    pylab.grid(which="minor", linestyle=":")
    pylab.tight_layout()


def main() -> None:
    # init
    # roy: Roy = Roy()
    roy: Roy3 = Roy3()
    agents_list: list[CarAgent] = roy.init_agents()
    iterations = roy.run(agents_list)

    # data for graph
    speed_time: list[int] = [i for i in range(back_sett.roy.iteration)]
    middle_speeds: list[float] = []
    # плотность
    flow_densities: list[float] = []
    # интенсивность
    flow_rates: list[float] = []
    changes_line: list[float] = []

    # data filling
    for agents in iterations:
        # средняя скорость
        speeds: list[float] = [agent.velocity for agent in agents]
        # middle_speed: float = float('{:.5f}'.format(sum(speeds) / len(speeds)))
        middle_speed: float = float((sum(speeds) / len(speeds)))
        middle_speeds.append(middle_speed)

        # функциональная диограмма
        count_car: int = sum([agent.track_complete for agent in agents])
        # flow_density: float = back_sett.roy.count_agent / back_sett.roy.track_length
        flow_density: float = 1000 * (
            count_car / back_sett.roy.track_length
            + (2 * rand.randint(0, 1) - 1) * (rand.random() / 10**8)
        )
        flow_rate: float = flow_density * middle_speed
        flow_densities.append(flow_density)
        flow_rates.append(flow_rate)

        # кол-во перестреоний
        count: float = sum([agent.changing_line for agent in agents])
        changes_line.append(count)

    # ^ кол-во перестреоний
    i: int = 2
    j: int = 3
    # строки - 2, столбца - 3, Текущая ячейка - 1
    pylab.subplot(i, j, 1)
    pylab.scatter(speed_time, changes_line, s=3)
    pylab.xlabel("t, c")
    pylab.ylabel("количество пересроений")
    # pylab.ylim([0, max(middle_speeds) + 2])

    # setting graph - 3
    _setting_graph()

    # ^ функциональная диограмма
    # строки - 1, столбца - 2, Текущая ячейка - 2
    pylab.subplot(i, j, 2)
    pylab.scatter(flow_densities, flow_rates, s=2)
    pylab.xlabel("p (1/м)")
    pylab.ylabel("q (1/с)")
    # pylab.ylim([0, 600])
    # pylab.xlim([0, 0.081])

    # setting graph - 2
    _setting_graph()

    # ^ средняя скорость
    # строки - 1, столбца - 2, Текущая ячейка - 1
    pylab.subplot(i, j, 3)
    pylab.plot(speed_time, middle_speeds)  # , alpha=0.8)
    pylab.xlabel("t, c")
    pylab.ylabel("v, м/с")
    pylab.ylim([0, max(middle_speeds) + 2])

    # setting graph - 1
    _setting_graph()

    # show graph
    pylab.show()


if __name__ == "__main__":
    main()
    # main2()
