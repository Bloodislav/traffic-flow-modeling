import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pygame

from frontend.models.car_front import CarFront
from frontend.models.map import Map

from data.dto import ImgPath, FrontRuntime, FrontObjects, BackRuntime


def init_front_objects(
    back: BackRuntime, imgs: ImgPath, hight: int, width: int
) -> FrontObjects:
    map: Map = Map(image_path=imgs.map, screen_height=hight, screen_width=width)
    user_car: CarFront = CarFront(image_path=imgs.user_car, model_car=back.car)
    ai_car_list: list[CarFront] = []

    for i in range(back.count_car):
        ai_car: CarFront = CarFront(imgs.ai_car, back.car_ai_list[i])
        ai_car_list.append(ai_car)

    return FrontObjects(map, user_car, ai_car_list, back.count_car)


def init_game_screen(
    back: BackRuntime, imgs: ImgPath, hight: int, width: int
) -> FrontRuntime:
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Modeling car")

    screen: pygame.Surface = pygame.display.set_mode((width, hight))
    main_front = pygame.font.SysFont("comicsans", 40)
    clock: pygame.time.Clock = pygame.time.Clock()
    front_object: FrontObjects = init_front_objects(back, imgs, hight, width)

    return FrontRuntime(screen, clock, main_front, hight, width, front_object)


def draw_object(runtime: FrontRuntime) -> None:
    runtime.screen.fill((0, 0, 0))
    runtime.objects.map.draw(runtime.screen)
    runtime.objects.user_car.draw(runtime.screen)

    for i in range(runtime.objects.count_car):
        runtime.objects.car_ai_list[i].draw(runtime.screen)
