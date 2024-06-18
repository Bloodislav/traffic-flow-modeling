import pygame
import math


class Map:
    def __init__(self, image_path: str, screen_width: int, screen_height: int) -> None:
        """Инициализация карты."""
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            self.image, (screen_width * 0.7, screen_height)
        )

        self.width: int = int(screen_width * 0.5)
        self.height: int = screen_height

        self.x: int = 0
        self.y: int = 0
        self.speed: float = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Инициализация карты."""
        for i in range(5):
            screen.blit(self.image, (self.x + self.width * i, self.y))
        screen.blit(self.image, (self.x - self.width, self.y))

    def update(self, car_speed: float, car_angle: float) -> None:
        """Обновление позиции."""
        self.speed = car_speed.real
        self.x -= int(math.cos(math.radians(-car_angle)) * self.speed)

        self.x = 0 if self.x <= -self.width else self.x
        self.x = -self.width if self.x >= self.width else self.x
