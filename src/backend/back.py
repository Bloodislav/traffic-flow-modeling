from models.car import Car, Car_AI
from models.map import Map
from models.dto import BackRuntime

def init_objects(width, height) -> BackRuntime:
    map: Map = Map(image_path="imgs/road.png", screen_width=width, screen_height=height)
    car: Car = Car(
        x=400, y=275, max_speed=25, angle=-90, image_path="imgs/red-car.png"
    )

    car_ai_list: list[Car_AI] = []
    count_car: int = 2
    for i in range(count_car - 1, -1, -1):
        car_ai: Car_AI = Car_AI(
            x=150 * (i + 1),
            y=275,
            max_speed=25,
            distance=150,
            angle=-90,
            image_path="imgs/white-car.png",
        )
        car_ai_list.append(car_ai)

    return BackRuntime(map, car, car_ai_list, count_car)