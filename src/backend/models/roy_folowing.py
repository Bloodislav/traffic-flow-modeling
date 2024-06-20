import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from numpy import random

from .roy3 import Roy3
from .car_agent import CarAgent
from .car2 import Car
from .car_ai2 import CarAi
from configs.config import setting


class RoyFollowing(Roy3):
    def __init__(self) -> None:
        super().__init__()
        
        self.following_car = setting.roy_follow.count_car
    
    def init_agents(self) -> list[CarAgent]:
        """Инициализация агентов на полосе"""
        agents: list[CarAgent] = []

        for i in range(self.count_agent):
            pos = i * setting.roy.track_length / self.count_agent * random.uniform(0, 5)
            agents.append(
                CarAgent(
                    pos=pos,
                    lane=random.randint(1, self.count_lanes - 1),
                )
            )
        
        pos = setting.roy.track_length
        agents.append(Car(pos, lane=self.count_lanes))
        
        for i in range(setting.roy_follow.count_car):
            pos = setting.roy.track_length - 2 * setting.following.length_car * i
            agents.append(CarAi(pos, lane=self.count_lanes))

        return agents