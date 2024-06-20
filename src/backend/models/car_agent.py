import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from numpy import random

from configs.config import setting
from dtos.dto import Pos


class CarAgent:
    def __init__(
        self,
        pos: float,
        lane: int,
    ) -> None:
        self.pos: float = pos
        self.new_pos: float = pos
        self.lane: int = lane

        self.max_velocity: float = setting.roy.max_velocity
        # self.velocity: float = setting.roy.max_velocity
        self.velocity: float = 0
        self.change_lane_l: float = setting.roy.change_line_l
        self.change_lane_r: float = setting.roy.change_line_r
        self.changing_line: bool = False
        self.ban: int = 0

        self.a_car_lead: float = 0  # i+
        self.a_car_back: float = 0  # i-

        self.distance: float = 0
        self.track_complete: bool = False
        
        self.distance_x: float = 0.0 

    # ---------------------------------------------------------------------------------------------------#
    def __new_velocity(self) -> float:
        """Обновление скорости"""
        return min(
            self.velocity + (self.a_car_lead + self.a_car_back), self.max_velocity
        )

    def __change_line(
        self,
        pos_r: Pos = None,
        pos_l: Pos = None,
    ):
        """Перестроение"""
        if setting.roy.count_lanes < 2:
            return

        if pos_r is not None:
            if (
                ((self.pos - pos_r.pos_slave) > 2 * self.max_velocity)
                and ((pos_r.pos_lead - self.pos) > self.__new_velocity())
                and ((pos_r.lead_velosity) > self.__new_velocity())
                and (random.random() <= self.change_lane_r)
            ):
                self.lane += 1
                self.changing_line = True
                self.ban = 3

        elif pos_l is not None:
            if (
                ((self.pos - pos_l.pos_slave) > 2 * self.max_velocity)
                and ((pos_l.pos_lead - self.pos) > self.__new_velocity())
                and ((pos_l.lead_velosity) > self.__new_velocity())
                and (random.random() <= self.change_lane_l)
            ):
                self.lane -= 1
                self.changing_line = True
                self.ban = 3

    def update_accel2(
        self,
        pos: Pos,
        pos_r: Pos = None,
        pos_l: Pos = None,
    ):
        l_back = self.pos - pos.pos_slave + setting.roy.length_agent
        self.a_car_back = (
            setting.roy.k_attraction / (setting.roy.r * l_back)
            if l_back < setting.roy.d_standart
            else 0
        )

        l_lead = pos.pos_lead - self.pos + setting.roy.length_agent
        self.a_car_lead = (
            setting.roy.k_attraction / l_lead
            if l_lead < setting.roy.d_standart
            else setting.roy.k_repulsion * l_lead
        )

        # возможность перестроения
        self.changing_line = False
        if (pos_r is not None) or (pos_l is not None):
            if (self.a_car_lead < 0) and (self.ban == 0):
                self.__change_line(pos_r, pos_l)
            else:
                self.ban -= 1 if self.ban > 0 else 0
        else:
            self.ban -= 1 if self.ban > 0 else 0

    # ---------------------------------------------------------------------------------------------------#

    def update_accel(self, pos_lead, pos_back):
        """Обновление ускорение относительно позиции"""
        l_back = self.pos - pos_back + setting.roy.length_agent
        self.a_car_back = (
            setting.roy.k_attraction / (setting.roy.r * l_back)
            if l_back < setting.roy.d_standart
            else 0
        )

        l_lead = pos_lead - self.pos + setting.roy.length_agent
        self.a_car_lead = (
            setting.roy.k_attraction / l_lead
            if l_lead < setting.roy.d_standart
            else setting.roy.k_repulsion * l_lead
        )

    def update_velocity(self):
        """Обновление скорости"""
        new_velocity: float = self.velocity + (self.a_car_lead + self.a_car_back)
        self.velocity = min(new_velocity, self.max_velocity)

    def new_pos_calc(self):
        """расчет новой позиции"""
        self.new_pos += self.velocity

    def update(self, track_length: float):
        """Обновление позиции"""
        self.new_pos = self.pos = self.pos + self.velocity

        self.distance += self.pos
        if self.distance >= track_length:
            self.distance -= track_length
            self.track_complete = True
        else:
            self.track_complete = False
