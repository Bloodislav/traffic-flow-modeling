import pygame

from data.dto import Runtime
from frontend.front import draw_object


def game_loop(runtime: Runtime) -> None:
    """Основной цикл игры."""
    running: bool = True
    fps: int = 60

    while running:
        runtime.front.clock.tick(fps)

        # 1. Update data
        runtime.back.car.move()
        runtime.back.car.update()
        runtime.front.objects.map.update(runtime.back.car.speed, runtime.back.car.angle)

        for ai_car in runtime.back.car_ai_list:
            ai_car.move()
            ai_car.update()

        # 2. User input
        runtime.front.objects.user_car.moving_car()
        running = quit()
        for event in pygame.event.get():
            running = not (event.type == pygame.QUIT)

        # 3. Draw objects
        draw_object(runtime.front)
        pygame.display.flip()

    pygame.quit()


def quit() -> bool:
    """Функция для управления игроком."""
    running: bool = True

    keys = pygame.key.get_pressed()

    # Выход из игры
    if keys[pygame.K_ESCAPE]:
        running = False

    return running
