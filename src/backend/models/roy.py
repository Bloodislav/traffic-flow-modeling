import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from numpy import random
from math import pi

from configs.config import setting
from .car_agent import CarAgent
from dtos.dto import Pos


class Roy:
    def __init__(self) -> None:
        """Инициализация"""
        self.iteration: int = setting.roy.iteration
        self.count_agent: int = setting.roy.count_agent
        self.count_lanes: int = setting.roy.count_lanes

    def __agent_accel_calc(self, agents: list[CarAgent], i: int):
        """Расчет ускорения агентов."""
        if i == 0:
            agents[i].update_accel(
                agents[i + 1].pos,
                agents[self.count_agent - 1].pos,
            )
        elif i == self.count_agent - 1:
            agents[i].update_accel(
                agents[0].pos,
                agents[i - 1].pos,
            )
        else:
            agents[i].update_accel(
                agents[i + 1].pos,
                agents[i - 1].pos,
            )

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

    def init_agents(self) -> list[CarAgent]:
        """Инициализация агентов на полосе"""
        agents: list[CarAgent] = []

        for i in range(self.count_agent):
            pos = i * setting.roy.track_length / self.count_agent * random.uniform(0, 5)
            agents.append(
                CarAgent(
                    pos=pos,
                    lane=random.randint(1, self.count_lanes),
                )
            )

        return agents

    def run(self, agents: list[CarAgent]):
        """Запуск алгоритма"""
        for _ in range(self.iteration):
            # Расчет предварительного ускорения + пересроение
            for i in range(self.count_agent):
                self.__agent_accel_calc(agents, i)
                agents[i].update_velocity()

            # Расчет новых положений
            for i in range(self.count_agent):
                agents[i].new_pos_calc()

            # Предотвращение столконовения
            for i in range(self.count_agent):
                self.__agent_velocity_calc(agents, i)
                agents[i].update(setting.roy.track_length)

            yield agents
