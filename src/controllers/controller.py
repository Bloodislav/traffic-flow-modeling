import pygame

from models.car import Car
from data.dto import Runtime
from frontend.front import draw_object


def game_loop(runtime: Runtime) -> None:
    """Основной цикл игры."""
    running: bool = True
    fps: int = 60
    dt: float = 1.6

    while running:
        runtime.front.clock.tick(fps)

        runtime.back.car.update(dt, runtime.front.width, runtime.front.hight)
        runtime.back.car_ai_list[0].move(
            dt,
            runtime.back.car.x,
            runtime.back.car.y,
            runtime.back.car.angle,
            runtime.front.width,
            runtime.front.hight,
        )

        for i in range(1, runtime.back.count_car):
            runtime.back.car_ai_list[i].move(
                dt,
                runtime.back.car_ai_list[i - 1].x,
                runtime.back.car_ai_list[i - 1].y,
                runtime.back.car_ai_list[i - 1].angle,
                runtime.front.width,
                runtime.front.hight,
            )

        running = move_player(runtime.back.car)
        for event in pygame.event.get():
            running = not (event.type == pygame.QUIT)

        draw_object(runtime)
        pygame.display.flip()

    pygame.quit()


def move_player() -> bool:
    """Функция для управления игроком."""
    running: bool = True
    
    keys = pygame.key.get_pressed()

    # Выход из игры
    if keys[pygame.K_ESCAPE]:
        running = False

    return running
