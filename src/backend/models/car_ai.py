from ..utils import ro_statment, v_h_statment
from car import Car


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
        super.__init__(self, x, y, max_speed, koeff)
        self.lead_car: Car = lead_car
        self.distance = distance
        self.curent_distance = distance
        
        self.a_accceler: float = 25.0
        self.b_accceler: float = 25.0

    def accelerate(self, ro: float, v_h: float):
        """Закон изменения ускорения по модели Трайбера"""
        self.acceleration = (
            ro * self.a_accceler * (1 - (self.speed / self.max_speed) ** 0.8) + 
            (1 - ro) * self.b_accceler * (v_h - self.speed)
        )
    
    def move(self) -> None:
        diff_x: int = self.lead_car.x - self.x
        diff_y: int = self.lead_car.y - self.y
        self.prev_speed = self.speed
        
        ro = ro_statment(diff_x, self.distance, 35)
        v_h = v_h_statment(diff_x, self.distance, self.max_speed)
        self.accelerate(ro, v_h)
        
        self.speed += float(self.acceleration.real)
        