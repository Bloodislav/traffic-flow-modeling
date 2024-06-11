import pygame

from data.dto import FrontRuntime, Runtime


def init_game_screen(hight: int, width: int) -> FrontRuntime:
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Modeling car")

    screen: pygame.Surface = pygame.display.set_mode((width, hight))
    main_front = pygame.font.SysFont("comicsans", 40)
    clock: pygame.time.Clock = pygame.time.Clock()

    return FrontRuntime(screen, clock, main_front, hight, width)


def draw_object(runtime: Runtime) -> None:
    runtime.front.screen.fill((0, 0, 0))
    runtime.back.map.draw(runtime.front.screen)
    runtime.back.car.draw(runtime.front.screen)

    for i in range(runtime.back.count_car):
        runtime.back.car_ai_list[i].draw(runtime.front.screen)
