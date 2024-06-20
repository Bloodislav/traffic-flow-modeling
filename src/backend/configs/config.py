from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from math import pi


class RoyConfig(BaseModel):
    # ! кол-во итераций алгоритма
    iteration: int = 80
    # ! кол-во акентов
    count_agent: int = 22
    # ! кол-во полос
    count_lanes: int = 3

    # ! радиус и длинна окржности [м]
    radius: float = 36
    track_length: float = 2 * pi * radius
    # ! длинна авто
    length_agent: float = 5.7

    # ! маскимальная скорость [м/с]
    """
        20 км/ч - 5,6 м/с
        60 км/ч - 16,7 м/с
        90 км/ч - 25 м/с
        130 км/ч - 36,1 м/с
    """
    max_velocity: float = 6.0
    # ! стандартная дистанция
    """
        20 км/ч — 2 м; 
        60 км/ч — 10 м; 
        90 км/ч — 25 м; 
        130 км/ч — 50 м; 
        < — 100 м
    """
    d_standart: int = 10

    # коээфициент притяжения
    k_repulsion: float = 0.301
    # коээфициент отталкивания
    k_attraction: float = 10.6
    # коэффициент, уменьшающий влияние позади идущего автомобиля
    r: float = 100
    # вероятность перестроения
    # change_line: float = 0.3
    change_line_r: float = 0.3
    change_line_l: float = 0.1
    # запрет на перестроение
    ban_change_line: int = 3


class Setting(BaseSettings):
    roy: RoyConfig = RoyConfig()


setting: Setting = Setting()
