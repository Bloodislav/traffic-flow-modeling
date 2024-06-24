import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from dtos.dto import Pos
from roy.car_agent import CarAgent
from configs.config import setting


class Car(CarAgent):
    def __init__(self, pos: float, lane: int) -> None:
        super().__init__(pos, lane)

        self.accel: float = 0
        self.prev_velocity: float = 0
        self.a_accceler: float = setting.following.a_accceler
        self.b_accceler: float = setting.following.b_accceler
        self.koeff: float = setting.following.koeff

        self.change_lane_l: float = setting.following.change_lane_l
        self.change_lane_r: float = setting.following.change_lane_r

        self.length = setting.following.length_car

    def update_velocity(self):
        new_velocity: float = self.velocity + self.accel
        self.velocity = min(new_velocity, self.max_velocity)

    def update_accel2(self, pos: Pos, pos_r: Pos = None, pos_l: Pos = None):
        self.accel = self.a_accceler * (
            1 - (self.prev_velocity / self.max_velocity) ** self.koeff
        )
