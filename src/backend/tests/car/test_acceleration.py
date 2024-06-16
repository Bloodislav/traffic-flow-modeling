from models.car import Car
from test_setting import car_object, a_accel


# ----=== Acceleration ===--- #
def test_a_x_1(car_object: Car, a_accel: int):
    car_object.accelerate_x(a_accel)
    assert car_object.a_x == a_accel


def test_a_x_2(car_object: Car, a_accel: int):
    car_object.accelerate_x(-a_accel)
    assert car_object.a_x == -a_accel


def test_a_y_1(car_object: Car, a_accel: int):
    car_object.accelerate_y(a_accel)
    assert car_object.a_y == a_accel


def test_a_y_2(car_object: Car, a_accel: int):
    car_object.accelerate_y(-a_accel)
    assert car_object.a_y == -a_accel
