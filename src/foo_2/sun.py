import pygame as pg
import math
import time

from pydantic import BaseModel
from dataclasses import dataclass


class Params(BaseModel):
    G: float = 6.6743e-11
    T: int = 1800
    scale: float = 6e8


@dataclass
class PlanetDTO:
    m: float
    x: float
    y: float


class Body:
    def __init__(
        self, m: float, x: float, y: float, vx: float, vy: float, R, color: str = "red"
    ):
        self.m: float = m  # масса тела в кг
        self.x: float = x  # начальная координата в м
        self.y: float = y  # начальная координата в м
        self.vx: float = vx  # начальная скорость по x в м/с
        self.vy: float = vy  # начальная скорость по y в м/с
        self.R = R  # радиус круга pygame в пикселях
        self.color: str = color  # цвет тела
        self.ax: float = 0
        self.ay: float = 0  # инициализируем ускорения сил, действующих на тело

    def iterate(self, objects: list[PlanetDTO], params: Params):
        self.ax = self.ay = 0  # обнуляем ускорение для пересчета
        # считаем ускорение от всех сил
        for obj in objects:
            temp: float = params.G * obj.m
            self.ax += (
                temp
                * (obj.x - self.x)
                / math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 3
            )
            self.ay += (
                temp
                * (obj.y - self.y)
                / math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 3
            )

        # по формуле равноускоренного движения считаем новую координату
        self.x += self.vx * params.T + self.ax * params.T**2 / 2
        self.y += self.vy * params.T + self.ay * params.T**2 / 2

        self.vx += self.ax * params.T  # считаем новую скорость в конце отрезка
        self.vy += self.ay * params.T


class System:
    def __init__(self, objects: list[Body], params: Params):
        self.objects: list[Body] = objects
        self.params: Params = params
        self.t: int = 0  # счетчик прошедшего времени

    def __convert(self, i: int):
        return [
            PlanetDTO(planet.m, planet.x, planet.y) for planet in self.objects[:i]
        ] + [
            PlanetDTO(planet.m, planet.x, planet.y) for planet in self.objects[i + 1 :]
        ]

    def iterate(self):
        for i, planet in enumerate(self.objects):
            planet_list = self.__convert(i)
            planet.iterate(planet_list, self.params)
        self.t += self.params.T

    def run(self, iteration):
        while self.t < iteration:
            for i, planet in enumerate(self.objects):
                planet_list = self.__convert(i)
                planet.iterate(planet_list, self.params)
            self.t += self.params.T
            yield self.objects


def convert(point, scale, DISPLAY):
    return (
        round(point[0] / scale + DISPLAY[0] / 2.0),
        round(-point[1] / scale + DISPLAY[1] / 2.0),
    )


def main():
    pg.init()
    DISPLAY = [700, 700]
    screen = pg.display.set_mode(DISPLAY)
    running = True

    params = Params()
    earth = Body(m=5.97e24, x=150e9, y=0, vx=0, vy=30000, R=5, color="blue")
    sun = Body(m=1.99e30, x=0, y=0, vx=0, vy=0, R=10, color="yellow")
    solar_system = System([earth, sun], params)

    n = 25
    count = 0
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if count % n == 0:
            screen.fill((20, 20, 20))
            for obj in solar_system.objects:
                pg.draw.circle(
                    screen,
                    obj.color,
                    convert((obj.x, obj.y), params.scale, DISPLAY),
                    obj.R,
                )
            pg.display.flip()

        solar_system.iterate()

        count += 1
        time.sleep(0.0001)

    pg.quit()


# import matplotlib.pyplot as plt
import pylab as plt


def _setting_graph():
    plt.minorticks_on()
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":")
    plt.tight_layout()


def graph():
    params = Params()
    earth = Body(m=5.97e24, x=150e9, y=0, vx=0, vy=30000, R=5, color="blue")
    sun = Body(m=1.99e30, x=0, y=0, vx=0, vy=0, R=10, color="yellow")
    solar_system = System([earth, sun], params)

    n = 20000
    iterations = n * params.T
    j = solar_system.run(iterations)

    times = [t for t in range(n)]
    axs_earth: list[float] = []
    ays_earth: list[float] = []
    axs_sun: list[float] = []
    ays_sun: list[float] = []

    x_earth: list[float] = []
    y_earth: list[float] = []

    vxs_earth: list[float] = []
    vys_earth: list[float] = []

    for objects in j:
        axs_earth.append(objects[0].ax)
        ays_earth.append(objects[0].ay)

        axs_sun.append(objects[1].ax)
        ays_sun.append(objects[1].ay)

        vxs_earth.append(objects[1].vx)
        vys_earth.append(objects[1].vy)

    # строки (i), столбца(j), Текущая ячейка
    i: int = 2
    j: int = 2

    plt.subplot(i, j, 1)
    _setting_graph()
    plt.plot(times, axs_earth, label="a_x")
    plt.plot(times, ays_earth, label="a_y")
    plt.xlabel("t, c")
    plt.ylabel("Ускорение")
    plt.legend(loc="upper left")
    plt.title("Изменения ускорения земли")

    plt.subplot(i, j, 2)
    _setting_graph()
    plt.plot(times, axs_sun, label="a_x")
    plt.plot(times, ays_sun, label="a_y")
    plt.xlabel("t, c")
    plt.ylabel("Ускорение")
    plt.legend(loc="upper left")
    plt.title("Изменения ускорения солнца")

    plt.subplot(i, j, 3)
    _setting_graph()
    plt.plot(times, vxs_earth, label="v_x")
    plt.plot(times, vys_earth, label="v_y")
    plt.xlabel("t, c")
    plt.ylabel("Скорость")
    plt.legend(loc="upper left")
    plt.title("Изменения скорости Земли")

    # show graph
    plt.show()


import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        graph()
    else:
        main()
