import pygame

from models.car import Car
from models.dto import Runtime
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


def move_player(car: Car) -> bool:
    """Функция для управления игроком."""
    running: bool = True
    moved: bool = False
    keys = pygame.key.get_pressed()

    a: float = 0.2 / 10
    b: float = 0.2 / 10

    # Ускорение
    if keys[pygame.K_d]:
        car.accelerate(a)
        moved = True
    # Замедление
    if keys[pygame.K_a]:
        car.accelerate(-0.01)
        moved = True
    # Поворот влево
    if keys[pygame.K_w]:
        car.turn(2.5)
        moved = True
    # Поворот вправо
    if keys[pygame.K_s]:
        car.turn(-2.5)
        moved = True
    # Остановка
    if keys[pygame.K_SPACE]:
        car.decelerate(b)
        moved = True
    # Выход из игры
    if keys[pygame.K_ESCAPE]:
        running = False

    # Замедление
    if not moved:
        car.decelerate(0.1) if ((car.speed > 0.1) or (car.speed < -0.1)) else car.stop()

    return running


