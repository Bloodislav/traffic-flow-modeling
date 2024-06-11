import math
import pygame

from utils.utils import blit_rotate_center
from utils.utils import ro_statment, v_h_statment


class Car_temp:
    def __init__(self) -> None:
        self.A: float
        self.B: float
        self.C: float
        self.x: float
        self.v: float
        self.a: float

    def update(self) -> None: ...


class Car:
    def __init__(
        self, x: int, y: int, max_speed: int, angle: int, image_path: str
    ) -> None:
        """Инициализация машины."""
        self.x: int = x
        self.y: int = y
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.image = pygame.transform.rotate(self.image, angle)
        self.speed: float = 0
        self.max_speed: int = max_speed
        self.angle: int = 0
        self.acceleration: float = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка машины на экране."""
        blit_rotate_center(screen, self.image, (self.x, self.y), self.angle)

    def accelerate(self, acceleration: float) -> None:
        """Ускорение автомобиля."""
        self.acceleration = acceleration

    def decelerate(self, deceleration: float) -> None:
        """Замедление автомобиля."""
        self.acceleration = deceleration * (self.speed < 0) - deceleration * (
            self.speed > 0
        )

    def turn(self, angle_change: float) -> None:
        """Поворот машины на заданный угол."""
        self.angle += int(angle_change * abs(self.speed / self.max_speed * 0.8))

    def stop(self) -> None:
        """Остановка машины."""
        self.speed, self.acceleration = [0, 0]

    def update(self, dt: float, screen_width: int, screen_height: int) -> None:
        """Обновление состояния автомобиля."""
        self.speed += self.acceleration * dt

        # Ограничиваем скорость максимальным значением
        if self.speed.real > self.max_speed:
            self.speed = self.max_speed
        elif self.speed.real < -self.max_speed / 1.5:
            self.speed = -self.max_speed / 1.5

        # Обновляем позицию автомобиля
        self.x += int(math.cos(math.radians(-self.angle)) * self.speed.real * dt)
        self.y += int(math.sin(math.radians(-self.angle)) * self.speed.real * dt)

        # Ограничения области передвижения
        self.x = int(screen_width * 0.8) if self.x > (screen_width * 0.8) else self.x
        self.x = int(screen_width * 0.1) if self.x < (screen_width * 0.1) else self.x

        self.y = (
            int(screen_height * 0.65) if self.y > (screen_height * 0.65) else self.y
        )
        self.y = int(screen_height * 0.3) if self.y < (screen_height * 0.3) else self.y


class Car_AI(Car):
    def __init__(
        self, x: int, y: int, max_speed: int, distance: int, angle: int, image_path: str
    ) -> None:
        """Инициализация машины."""
        super().__init__(x, y, max_speed, angle, image_path)
        self.distance = distance
        self.curent_distance = distance
        self.prev_speed: int = 0

    def accelerate(self, ro: float, v_h: float):
        a: float = 3 / 10
        b: float = 10 / 10

        self.acceleration = ro * a * (1 - (self.speed / self.max_speed) ** 0.8) + (
            1 - ro
        ) * b * (v_h - self.speed)

    def move(
        self,
        dt: float,
        x_forward: int,
        y_forward: int,
        angle_forward: int,
        screen_width: int,
        screen_height: int,
    ) -> None:
        """Расчет передвижения"""
        diff_x = x_forward - self.x

        self.prev_speed = self.speed
        ro = ro_statment(diff_x, self.distance, 50)
        v_h = v_h_statment(diff_x, self.distance, self.max_speed)
        self.accelerate(ro, v_h)

        self.speed += float(self.acceleration.real)
        self.update(dt * 0.8, screen_width, screen_height)
