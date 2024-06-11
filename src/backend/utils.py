import numpy as np
from math import pow
from scipy.interpolate import interp1d


def ro_statment(h: float, h_max: float, d: float) -> float:
    """"""
    res: float = 0
    if h_max + d >= h >= h_max:
        temp = ((h - h_max) / d) - 1
        res = -2 * pow(temp, 3) - 3 * pow(temp, 2) + 1
    elif h > h_max:
        res = 1

    return res


def v_h_statment(h: float, h_max: float, max_speed: int) -> float:
    """"""
    res: float = 0
    x = np.array([0, 5, 20, 45, 80, 120, 200, 1000])
    y = np.array([0, 25, 50, 75, 105, 125, 201, 1000])
    f2 = interp1d(x, y, kind="cubic")

    if h > h_max:
        temp: float = pow((h - h_max) / f2(h), 3)
        res = max_speed * (temp / (1 + temp))

    return res.real
