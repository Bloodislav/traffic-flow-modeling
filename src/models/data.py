from dataclasses import dataclass


@dataclass
class ConfigCar:
    # эффективная мощность двигателя, кВт
    Nemaх: int = 154
    Rd: float = 0.405
    Ga: int = 117700
    nmin: int = 700

    Kp: float = 0.8
    Kb: float = 0.5
    fo: float = 0.02
    # максимальная частота вращения коленчатого вала двигателя, 1/с
    nmax: int = 2600

    KPD: float = 0.9
    F: float = 6.891
    # частота вращения коленчатого вала двигателя при максимальной мощности, 1/с
    nN: int = 2300
    Mkmax: float = 780 / (1400)

    Rk: float = 0.42
    Kf: float = 0.000007
    slope: float = 0
    Ugl: float = 5.73

    А: float = 0.6879
    B: float = 1.7478
    С: float = 1.4357

    # передаточное число коробки передач
    U1: float = 3.364
    U2: float = 1.909
    U3: float = 1.421
    U4: float = 1.0
    U5: float = 0.652
    U6: float = 0.615


@dataclass
class ConfigModle:
    delta_t: float = 0.4
