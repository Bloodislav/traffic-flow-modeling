from dataclasses import dataclass

from models.car import Car, Car_AI
from models.map import Map
from pygame.font import Font
from pygame.time import Clock
from pygame import Surface


@dataclass
class FrontRuntime:
    screen: Surface
    clock: Clock
    main_font: Font
    hight: int
    width: int


@dataclass
class BackRuntime:
    map: Map
    car: Car
    car_ai_list: list[Car_AI]
    count_car: int


@dataclass
class Runtime:
    front: FrontRuntime
    back: BackRuntime
