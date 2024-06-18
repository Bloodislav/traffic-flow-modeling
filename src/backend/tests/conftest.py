from models.car import Car
from models.car_ai import CarAi
import pytest


@pytest.fixture(scope="function")
def car_object() -> Car:
    return Car(x=40, y=0, max_speed=17, koeff=1.01)

@pytest.fixture(scope="function")
def car_ai_object(car_object: Car) -> CarAi:
    return CarAi(
        x=0,
        y=0,
        max_speed=17, 
        koeff=1.01,
        lead_car=car_object,
    )

@pytest.fixture(scope="function")
def a_accel() -> int:
    return 2
