from dataclasses import dataclass
from pygame.font import Font
from pygame.time import Clock
from pygame import Surface

from backend.models.following.car import Car
from backend.models.following.car_ai import CarAi

from frontend.models.map import Map
from frontend.models.car_front import CarFront


@dataclass
class ImgPath:
    user_car: str
    map: str
    ai_car: str


@dataclass
class FrontObjects:
    map: Map
    user_car: CarFront
    car_ai_list: list[CarFront]
    count_car: int


@dataclass
class FrontRuntime:
    # settings screen
    screen: Surface
    clock: Clock
    main_font: Font
    hight: int
    width: int
    objects: FrontObjects


@dataclass
class BackRuntime:
    car: Car
    car_ai_list: list[CarAi]
    count_car: int


@dataclass
class Runtime:
    front: FrontRuntime
    back: BackRuntime
