import numpy as np
from math import pow
from scipy.interpolate import interp1d

from .car import Car


class CarAi(Car):
    def __init__(
        self,
        x: int,
        y: int,
        max_speed: float,
        koeff: float,
        lead_car: Car,
        distance: int,
    ) -> None:
        """Инициализация ии_машины."""
        super().__init__(x, y, max_speed, koeff)
        self.lead_car: Car = lead_car
        self.distance = distance
        self.curent_distance = distance

    def ro_func(self, h: float, h_max: float, d: float) -> float:
        """"""
        res: float = 0
        if h_max + d >= h >= h_max:
            temp = ((h - h_max) / d) - 1
            res = -2 * pow(temp, 3) - 3 * pow(temp, 2) + 1
        elif h > h_max:
            res = 1

        return res

    def v_h_func(self, h: float, h_max: float, max_speed: int) -> float:
        """"""
        res: float = 0
        x = np.array([0, 5, 20, 45, 80, 120, 200, 1000])
        y = np.array([0, 25, 50, 75, 105, 125, 201, 1000])
        f2 = interp1d(x, y, kind="cubic")

        if h > h_max:
            temp: float = pow((h - h_max) / f2(h), 3)
            res = max_speed * (temp / (1 + temp))

        return res.real

    def accelerate(self) -> None:
        """Закон изменения ускорения по модели следования за лидером"""
        diff_x: int = self.lead_car.x - self.x
        ro = self.ro_func(diff_x, self.distance, 35)
        v_h = self.v_h_func(diff_x, self.distance, self.max_speed)

        koef_1 = self.a_accceler * (1 - (self.speed / self.max_speed) ** self.koeff)
        koef_2 = self.b_accceler * (self.speed - v_h)

        if self.lead_car.speed.real >= 0:
            self.acceleration = (ro) * koef_1 + (ro - 1) * koef_2
        else:
            self.acceleration = (ro - 1) * koef_1 - (ro) * koef_2

    def move(self) -> None:
        diff_y: int = self.lead_car.y - self.y

        self.prev_speed = self.speed
        self.accelerate()
        self.speed += float(self.acceleration.real)
