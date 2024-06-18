from .models.car import Car
from .models.car_ai import CarAi
from data.dto import BackRuntime

# TODO DTO - Setting_model


def init_objects() -> BackRuntime:
    count_car: int = 4
    car_length: float = 4.0
    max_speed: float = 17.0
    koeff: float = 1.01

    x: int = count_car * 2 * car_length
    y: int = 0

    car: Car = Car(x + 2 * car_length, y, max_speed, koeff)
    car_ai_list: list[CarAi] = [
        CarAi(x, y, max_speed, koeff, car),
    ]

    for i in range(1, count_car):
        car_ai: CarAi = CarAi(
            x=x - i * 2 * car_length,
            y=y,
            max_speed=max_speed,
            koeff=koeff,
            lead_car=car_ai_list[i - 1],
        )
        car_ai_list.append(car_ai)

    return BackRuntime(car, car_ai_list, count_car)
