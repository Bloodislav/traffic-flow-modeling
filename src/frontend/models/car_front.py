import pygame
from typing import Union

from ..utils import blit_rotate_center

from backend.models.car import Car
from backend.models.car_ai import CarAi


class CarFront:
    def __init__(self, image_path: str, model_car: Union[Car | CarAi]) -> None:
        """Инициализация класса для отрисовки"""
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.model: Union[Car | CarAi] = model_car
        self.image = pygame.transform.rotate(self.image, -90)

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка машины на экране."""
        blit_rotate_center(
            screen, self.image, (self.model.x, self.model.y), self.model.angle
        )

    def update_model(self) -> None:
        """Обновление данных в модели."""
        self.model.move()
        self.model.update()

    def moving_car(self) -> None:
        """Перемещения лидирующей машины."""
        keys = pygame.key.get_pressed()
        moved: bool = False

        a: float = self.model.a_accceler / 10
        b: float = self.model.b_accceler / 10
        angle: float = 2.5

        # Ускорение
        if keys[pygame.K_d]:
            self.model.accelerate(1, a)
            moved = True

        # Замедление
        if keys[pygame.K_a]:
            self.model.accelerate(-1, a)
            moved = True

        # Поворот влево
        if keys[pygame.K_w]:
            self.model.turn(angle)
            moved = True

        # Поворот вправо
        if keys[pygame.K_s]:
            self.model.turn(-angle)
            moved = True

        # Остановка
        if keys[pygame.K_SPACE]:
            if self.model.speed.real > 0:
                self.model.accelerate(-1, b)
                moved = True
            elif self.model.speed.real < 0:
                self.model.accelerate(1, b)
                moved = True

        # Замедление
        if not moved:
            (
                self.model.accelerate(0, 0.1)
                if ((self.model.speed.real > 0.1) or (self.model.speed.real < -0.1))
                else self.model.stop()
            )
