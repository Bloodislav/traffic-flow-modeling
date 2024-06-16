from models.car import Car
import pytest


@pytest.fixture
def car_object() -> Car:
    return Car(x=0, y=0, max_speed=17, koeff=1.01)


@pytest.fixture
def a_accel() -> int:
    return 2
