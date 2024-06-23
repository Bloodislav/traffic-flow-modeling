from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from math import pi


class RoyConfig(BaseModel):
    # ! кол-во итераций алгоритма
    iteration: int = 500
    # ! кол-во акентов
    count_agent: int = 220
    # ! кол-во полос
    count_lanes: int = 3

    # ! радиус и длинна окржности [м]
    radius: float = 360
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
    max_velocity: float = 25
    # ! стандартная дистанция
    """
        20 км/ч — 2 м; 
        60 км/ч — 10 м; 
        90 км/ч — 25 м; 
        130 км/ч — 50 м; 
        < — 100 м
    """
    d_standart: int = 25

    # коээфициент притяжения
    k_repulsion: float = 0.301
    # коээфициент отталкивания
    k_attraction: float = 10.6
    # коэффициент, уменьшающий влияние позади идущего автомобиля
    r: float = 100
    # вероятность перестроения
    # change_line: float = 0.3
    change_line_r: float = 0.3
    change_line_l: float = 0.3
    # запрет на перестроение
    ban_change_line: int = 3


class CarFollowing(BaseModel):
    t_driver: float = 0.87
    c_road: float = 0.053
    koeff: float = 1.01
    
    a_accceler: float = 2.5
    b_accceler: float = 2.5
    
    change_lane_l: float = 0
    change_lane_r: float = 0
    
    length_car: float = 5.7

class RoyFollowing(BaseModel):
    count_car: int = 5

class Setting(BaseSettings):
    roy: RoyConfig = RoyConfig()
    following: CarFollowing = CarFollowing()
    roy_follow: RoyFollowing = RoyFollowing()

setting: Setting = Setting()
