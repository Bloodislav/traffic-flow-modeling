import math


class Car:
    """Класс машины с описание закона движения"""

    def __init__(
        self,
        x: int,
        y: int,
        max_speed: float,
        koeff: float,
    ) -> None:
        """Инициализация машины."""
        self.x: int = x
        self.y: int = y
        self.koeff: float = koeff
        self.max_speed: float = max_speed

        self.angle: int = 0
        self.speed: float = 0
        self.prev_speed: float = 0
        self.acceleration: float = 0

    def accelerate(self, turn: int, acceleration: float) -> None:
        """Ускорение / замедление автомобиля."""
        if turn > 0:
            self.acceleration = acceleration * (
                1 - (self.prev_speed / self.max_speed) ** self.koeff
            )
        elif self.speed != 0:
            self.acceleration = acceleration if self.speed < 0 else -acceleration

    def stop(self) -> None:
        """Остановка машины."""
        self.speed, self.acceleration = [0, 0]

    def move(self) -> None:
        """Обмновление скорости"""
        self.prev_speed = self.speed
        self.speed += self.acceleration
    
    def update(self) -> None:
        # Ограничиваем скорость максимальным значением
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < -self.max_speed / 1.5:
            self.speed = -self.max_speed / 1.5
        
        # Обновляем позицию автомобиля
        self.x += int(math.cos(math.radians(-self.angle)) * self.speed)
        self.y += int(math.sin(math.radians(-self.angle)) * self.speed)
