import numpy as np
from math import pow
from scipy.interpolate import interp1d
from scipy.integrate import quad

from dtos.dto import Pos
from .car2 import Car
from configs.config import setting


class CarAi(Car):
    def __init__(self, pos: float, lane: int) -> None:
        super().__init__(pos, lane)
        
        # self.distance_x: float = 0
        
    # ---=== Another ===--- #
    def __ro_func(self, h: float, h_max: float, d: float) -> float:
        """"""
        res: float = 0
        if h_max + d >= h >= h_max:
            temp = ((h - h_max) / d) - 1
            res = -2 * pow(temp, 3) - 3 * pow(temp, 2) + 1
        elif h > h_max:
            res = 1

        return res
    
    def __v_h_func(self, h: float, h_max: float, max_speed: int) -> float:
        """"""
        res: float = 0
        x = np.array([0, 5, 20, 45, 80, 120, 200, 1000])
        y = np.array([5, 25, 50, 75, 105, 125, 201, 1000])
        f2 = interp1d(x, y, kind="cubic")

        if h > h_max:
            temp: float = pow((h - h_max) / f2(h), 3)
            res = max_speed * (temp / (1 + temp))

        return res.real
    
    def __target_function_f(self, x) -> float:
        return self.lead_car.speed_x - self.speed_x
    
    # ---=== Accelerate | Speed ===--- #
    def __need_distance(self) -> None:
        self.distance_x = (
            self.length
            + 2.2 * self.prev_velocity
            + (1 / 2.5 - 1 / self.b_accceler)
            * self.prev_velocity**2 / 2 * 1.1
            
            # self.length
            # + setting.following.t_driver * self.prev_velocity
            # + setting.following.c_road * self.prev_velocity**2
        )
    
    def update_accel2(
        self,
        pos: Pos,
        pos_r: Pos = None,
        pos_l: Pos = None,
    ):
        self.__need_distance()
        diff_x: int = pos.pos_lead - self.pos
        
        # diff_x_v: float = quad(self.__target_function_f, 0, self.max_velocity)
        # diff_x_v = diff_x_v[0]
        
        ro = self.__ro_func(diff_x, self.distance_x, self.distance_x / 2)
        v_h = self.__v_h_func(diff_x, self.distance_x, self.max_velocity)

        koef_1 = self.a_accceler * (1 - (self.prev_velocity / self.max_velocity) ** self.koeff)
        koef_2 = self.b_accceler * (self.velocity - v_h)
        
        self.accel = (ro) * koef_1 + (ro - 1) * koef_2
        self.accel = (
            self.accel if self.accel * setting.following.t_driver ** 2 
            / self.length >= 0  else 0
            # / self.distance_x >= 0  else 0
        )
