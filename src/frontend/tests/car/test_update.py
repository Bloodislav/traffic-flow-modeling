import pytest
from models.car import Car


# ----=== Uppdate ===--- #
def test_update_x_1(car_object: Car, a_accel: int):
    car_object.accelerate_x(a_accel)
    car_object.update()

    assert car_object.y == 0
    assert car_object.x == a_accel
    assert car_object.speed_x > 0


def test_update_x_2(car_object: Car, a_accel: int):
    car_object.accelerate_x(a_accel)

    for _ in range(5):
        car_object.update()

    assert car_object.y == 0
    assert car_object.x > 0
    assert car_object.speed_x == 0


def test_update_x_3(car_object: Car, a_accel: int):
    n = 20
    for _ in range(n // 2):
        car_object.accelerate_x(a_accel)
        car_object.update()
    for _ in range(n // 2):
        car_object.update()
    assert car_object.x > 0
    assert car_object.speed_x > 0


def test_update_compex_1(car_object: Car, a_accel: int):
    car_object.accelerate_x(a_accel)
    car_object.accelerate_y(a_accel)

    car_object.update()
    assert car_object.x == a_accel
    assert car_object.y == a_accel

    assert car_object.speed_x == a_accel - car_object.speed_stop
    assert car_object.speed_y == a_accel - car_object.speed_stop


def test_update_compex_2(car_object: Car, a_accel: int):
    n = 20

    for _ in range(n):
        car_object.accelerate_x(a_accel)
        car_object.accelerate_y(a_accel)
        car_object.update()

    assert car_object.x == 201
    assert car_object.y == 59
    assert car_object.speed_x > 15
    assert car_object.speed_y >= 3
