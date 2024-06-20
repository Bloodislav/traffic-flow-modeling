import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from numpy import random

from roy import Roy
from car_agent import CarAgent
from configs.config import setting
from dtos.dto import Pos


class Roy2(Roy):
    def __agent_accel_calc(self, agents: list[list[CarAgent]], j: int, i: int):
        """Расчет ускорения агентов."""
        neighbors_rigth: int = None
        neighbors_left: int = None
        neighbors_rigth, neighbors_left = (
            [j + 1, None]
            if j == 0
            else [None, j - 1] if j == len(agents) - 1 else [j + 1, j - 1]
        )

        indx_lead: int = None
        indx_slave: int = None
        pos: Pos = None
        pos_r: Pos = None
        pos_l: Pos = None

        def __indxs(count_agents):
            indx_lead, indx_slave = (
                [i + 1, count_agents - 1]
                if i == 0
                else [0, i - 1] if i == count_agents - 1 else [i + 1, i - 1]
            )
            return indx_lead, indx_slave

        indx_lead, indx_slave = __indxs(len(agents[j]))
        pos = Pos(
            agents[j][indx_lead].pos,
            agents[j][indx_slave].pos,
            agents[j][indx_lead].velocity,
        )

        if neighbors_rigth:
            indx_lead, indx_slave = __indxs(len(agents[neighbors_rigth]))
            pos_r = Pos(
                agents[neighbors_rigth][indx_lead].pos,
                agents[neighbors_rigth][indx_slave].pos,
                agents[neighbors_rigth][indx_lead].velocity,
            )

        if neighbors_left:
            indx_lead, indx_slave = __indxs(len(agents[neighbors_left]))
            pos_l = Pos(
                agents[neighbors_left][indx_lead].pos,
                agents[neighbors_left][indx_slave].pos,
                agents[neighbors_left][indx_lead].velocity,
            )

        agents[j][i].update_accel2(pos, pos_r, pos_l)

        if agents[j][i].changing_line:
            n_j = agents[j][i].lane - 1
            car = agents[j].pop(i)
            agents[n_j].insert(indx_lead, car)

    def init_agents(self, count_lines: int) -> list[list[CarAgent]]:
        """Инициализация агентов на полосе"""
        result: list[list[CarAgent]] = []
        for j in range(1, count_lines + 1):
            agents: list[CarAgent] = []
            prev_pos: float = 0
            pos: float = 0

            for i in range(self.count_agent):
                prev_pos = pos
                pos = (
                    i
                    * setting.roy.track_length
                    / self.count_agent
                    * random.uniform(0, 5)
                )
                # pos = (
                #     pos
                #     if pos - prev_pos > 2 * setting.roy.length_agent
                #     else prev_pos + 2 * setting.roy.length_agent
                # )

                agents.append(CarAgent(pos=pos, lane=j))
            result.append(agents)

        return result

    def run(self, agents: list[list[CarAgent]]):
        """Запуск алгоритма"""
        # for j in range(len(agents)):
        for _ in range(self.iteration):
            # Расчет предварительного ускорения + пересроение
            i = 0
            while i < len(agents[0]):
                self.__agent_accel_calc(agents, 0, i)
                i += 1

            for i in range(len(agents[1])):
                self.__agent_accel_calc(agents, 1, i)

            for i in range(len(agents[0])):
                agents[0][i].update_velocity()
            for i in range(len(agents[1])):
                agents[1][i].update_velocity()

            # Расчет новых положений
            for i in range(len(agents[0])):
                agents[0][i].new_pos_calc()
            for i in range(len(agents[1])):
                agents[1][i].new_pos_calc()

            # Предотвращение столконовения
            for i in range(len(agents[0])):
                self.__agent_velocity_calc(agents[0], i)
                agents[0][i].update(setting.roy.track_length)

            for i in range(len(agents[1])):
                self.__agent_velocity_calc(agents[1], i)
                agents[1][i].update(setting.roy.track_length)

            yield agents
