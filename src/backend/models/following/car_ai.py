import numpy as np
from math import pow
from scipy.interpolate import interp1d
from scipy.integrate import simps, quad

from .car import Car

class CarAi(Car):
    def __init__(
        self,
        x: int,
        y: int,
        max_speed: float,
        koeff: float,
        lead_car: Car,
    ) -> None:
        """Инициализация ии_машины."""
        super().__init__(x, y, max_speed, koeff)
        self.lead_car: Car = lead_car
        self.distance_x: float = 0
        self.distance_y: float = 10

    # ---=== Another ===--- #
    def ro_func(self, h: float, h_max: float, d: float) -> float:
        """Весовая функция"""
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
        y = np.array([5, 25, 50, 75, 105, 125, 201, 1000])
        f2 = interp1d(x, y, kind="cubic")

        if h > h_max:
            temp: float = pow((h - h_max) / f2(h), 3)
            res = max_speed * (temp / (1 + temp))

        return res.real

    # ------ Cord X ------
    def _need_distance(self) -> None:
        self.distance_x = (
            2 * self.length
            + 2.2 * self.prev_speed_x
            + (1 / self.lead_car.b_accceler - 1 / self.b_accceler)
            * 1.1 * self.prev_speed_x**2
        )

    def target_function_f(self, x) -> float:
        return self.lead_car.speed_x - self.speed_x

    def accelerate_ai_x(self) -> None:
        self._need_distance()

        diff_x: int = self.lead_car.x - self.x
        diff_x_v: float = quad(self.target_function_f, 0, self.max_speed_x)
        diff_x_v = diff_x_v[0]

        ro = self.ro_func(diff_x, self.distance_x, 4 * self.length)
        # v_h = self.v_h_func(diff_x_v, self.distance_x, self.max_speed_x)
        v_h = self.v_h_func(diff_x, 2 * self.length, self.max_speed_x)

        koef_1 = self.a_accceler * (
            1 - (self.prev_speed_x / self.max_speed_x) ** self.koeff
        )
        koef_2 = self.b_accceler * (self.speed_x - v_h)

        if self.lead_car.speed_x.real >= 0:
            self.a_x = (ro) * koef_1 + (ro - 1) * koef_2
        else:
            self.a_x = (ro - 1) * koef_1 - (ro) * koef_2

        self.a_x = self.a_x if self.a_x * 1.6**2 / 2 * self.length >= 0.0 else 0

    # ------ Cord Y ------ #
    def accelerate_ai_y(self) -> None:
        diff_y: int = self.lead_car.y - self.y
        ro = self.ro_func(diff_y, 2, 15)
        v_h = self.v_h_func(diff_y, 2, self.max_speed_y)

        koef_1 = self.a_accceler * (
            1 - (self.prev_speed_y / self.max_speed_y) ** self.koeff
        )
        koef_2 = self.b_accceler * (self.speed_y - v_h)

        if self.lead_car.speed_y.real >= 0:
            self.a_y = (ro) * koef_1 + (ro - 1) * koef_2
        else:
            self.a_y = (ro - 1) * koef_1 - (ro) * koef_2

        self.a_y = self.a_y if abs(self.a_y.real * 0.87**2 / 2) >= 0.3 else 0

    # ---=== Move ===--- #
    def move(self) -> None:
        self.prev_speed_x = self.speed_x
        self.prev_speed_y = self.speed_y

        self.accelerate_ai_x()
        self.accelerate_ai_y()

        self.speed_x += float(self.a_x.real)
        self.speed_y += float(self.a_y.real)
