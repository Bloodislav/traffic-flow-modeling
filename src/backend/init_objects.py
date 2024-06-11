from .models.car import Car
from .models.car_ai import CarAi
from data.dto import BackRuntime


def init_objects() -> BackRuntime:
    car: Car = Car(500, 275, 25.0, 1.01)

    distance: int = 100

    car_ai_list: list[CarAi] = [
        CarAi(400, 275, 25.0, 1.01, car, distance),
    ]
    count_car: int = 4

    for i in range(1, count_car):
        car_ai: CarAi = CarAi(
            x=100 * (count_car - i),
            y=275,
            max_speed=25.0,
            koeff=1.01,
            lead_car=car_ai_list[i - 1],
            distance=distance,
        )
        car_ai_list.append(car_ai)

    return BackRuntime(car, car_ai_list, count_car)
