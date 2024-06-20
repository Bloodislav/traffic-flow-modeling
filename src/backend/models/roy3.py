import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from numpy import random

from .roy import Roy
from .car_agent import CarAgent
from configs.config import setting
from dtos.dto import Pos


class Roy3(Roy):
    def __indxs(self, count_agents: int, i: int):
        indx_lead, indx_slave = (
            [i + 1, count_agents - 1]
            if i == 0
            else [0, i - 1] if i == count_agents - 1 else [i + 1, i - 1]
        )
        return indx_lead, indx_slave

    def __indxs_slave(self, count_agents: int, indx_lead: int):
        indx_slave = count_agents - 1 if indx_lead == 0 else indx_lead - 1
        return indx_lead, indx_slave

    def __find_agent(self, agents: list[CarAgent], pos: float, line: int):
        for indx, agent in enumerate(agents):
            if (agent.pos > pos) and (agent.lane == line):
                return indx

        return 0

    def __get_temp_agent(self, agents: list[CarAgent], line: int) -> list[CarAgent]:
        return [agent for agent in agents if agent.lane == line]

    def __agent_accel_calc(
        self,
        temp_agents: list[CarAgent],
        agents: list[CarAgent],
        line: int,
        i: int,
    ):
        """Расчет ускорения агентов."""
        # Расчет соседних полос
        neighbors_rigth: int = None
        neighbors_left: int = None

        neighbors_rigth, neighbors_left = (
            [line + 1, None]
            if line == 1
            else (
                [None, line - 1]
                if line == setting.roy.count_lanes
                else [line + 1, line - 1]
            )
        )

        position: float = temp_agents[i].pos
        indx_lead: int = None
        indx_slave: int = None
        pos_r: Pos = None
        pos_l: Pos = None

        indx_lead = 0 if i == len(temp_agents) - 1 else i + 1
        indx_slave = len(temp_agents) - 1 if i == 0 else i - 1
        pos: Pos = Pos(
            temp_agents[indx_lead].pos,
            temp_agents[indx_slave].pos,
            temp_agents[indx_lead].velocity,
        )

        if neighbors_rigth is not None:
            temp: list[CarAgent] = self.__get_temp_agent(agents, neighbors_rigth)
            if len(temp) > 1:
                indx_lead = self.__find_agent(temp, position, neighbors_rigth)
                indx_slave = len(temp) - 1 if indx_lead == 0 else indx_lead - 1
                pos_r = Pos(
                    temp[indx_lead].pos,
                    temp[indx_slave].pos,
                    temp[indx_lead].velocity,
                )

        if neighbors_left is not None:
            temp: list[CarAgent] = self.__get_temp_agent(agents, neighbors_left)
            if len(temp) > 1:
                indx_lead = self.__find_agent(temp, position, neighbors_left)
                indx_slave = len(temp) - 1 if indx_lead == 0 else indx_lead - 1
                pos_l = Pos(
                    temp[indx_lead].pos,
                    temp[indx_slave].pos,
                    temp[indx_lead].velocity,
                )

        temp_agents[i].update_accel2(pos, pos_r, pos_l)

    def __get_agents(self, agents: list[CarAgent]):
        for j in range(1, self.count_lanes + 1):
            yield [agent for agent in agents if agent.lane == j]

    def __is_agent_overtook_lead(self, pos: float, lead_pos: float) -> bool:
        """Агент обогнал лидера"""
        return pos >= lead_pos

    def __agent_velocity_calc(self, agents: list[CarAgent], i: int):
        """Расчет скорости агента с учетом обгона."""
        lead_indx = 0 if i == len(agents) - 1 else i + 1

        new_velocity = (
            agents[i].velocity - 1 - (agents[i].new_pos - agents[lead_indx].pos)
        )
        new_velocity = (
            min(new_velocity, setting.roy.max_velocity) if new_velocity > 0.01 else 0
        )
        agents[i].velocity = (
            agents[i].velocity
            if self.__is_agent_overtook_lead(
                agents[i].new_pos, agents[lead_indx].new_pos
            )
            else new_velocity
        )

    def run(self, agents: list[CarAgent]):
        """Запуск алгоритма"""
        result: list[CarAgent] = []
        for _ in range(self.iteration):
            t_agents = agents.copy()

            for temp in self.__get_agents(agents):
                # Расчет предварительного ускорения + пересроение
                temp_agent = temp.copy()
                count_agents: int = len(temp_agent)

                if count_agents != 0:
                    line: int = temp_agent[0].lane

                    for i in range(count_agents):
                        self.__agent_accel_calc(temp_agent, t_agents, line, i)
                        temp_agent[i].update_velocity()
                    line
                    # Расчет новых положений
                    for i in range(count_agents):
                        temp_agent[i].new_pos_calc()
                    line
                    # Предотвращение столконовения
                    for i in range(count_agents):
                        self.__agent_velocity_calc(temp_agent, i)
                        temp_agent[i].update(setting.roy.track_length)
                    line
                # result += temp_agent
                result = list(set(result + temp_agent))

            # ! filter by pos
            agents = result.copy()
            yield agents
