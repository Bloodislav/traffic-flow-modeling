from ..utils import ro_statment, v_h_statment, v_h_statment_reverse
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

    def accelerate(self, ro: float, v_h: float):
        """Закон изменения ускорения по модели Трайбера"""
        self.acceleration = ro * self.a_accceler * (
            1 - (self.speed / self.max_speed) ** 0.8
        ) + (1 - ro) * self.b_accceler * (v_h - self.speed)

        self.acceleration *= -1 if self.lead_car.speed.real < 0 else 1

    def move(self) -> None:
        diff_x: int = self.lead_car.x - self.x
        diff_y: int = self.lead_car.y - self.y
        self.prev_speed = self.speed

        ro = ro_statment(diff_x, self.distance, 35)
        v_h = v_h_statment(diff_x, self.distance, self.max_speed)

        if self.lead_car.speed.real < 0:
            ro, v_h = 1 / (1 + ro), 1 / (1 + v_h)
            self.accelerate(v_h, ro)
        else:
            self.accelerate(ro, v_h)

        print(f"{v_h=}, {ro=}, {self.acceleration=}")

        self.speed += float(self.acceleration.real)
