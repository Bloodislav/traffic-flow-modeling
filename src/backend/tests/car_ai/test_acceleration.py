from models.car_ai import CarAi


# ----=== Acceleration ===--- #
def test_a_x_1(car_ai_object: CarAi):
    car_ai_object.accelerate_ai_x()
    assert car_ai_object.a_x > 0


def test_a_x_2(car_ai_object: CarAi, a_accel: int):
    ...
    # assert car_ai_object.a_x < 0


# TODO
def test_a_y_1(car_ai_object: CarAi, a_accel: int):
    car_ai_object.accelerate_y(a_accel)
    car_ai_object.lead_car.update()
    car_ai_object.update()

    # assert car_ai_object.a_y == a_accel


def test_a_y_2(car_ai_object: CarAi, a_accel: int):
    car_ai_object.accelerate_y(-a_accel)
    car_ai_object.lead_car.update()
    car_ai_object.update()

    # assert car_ai_object.a_y == -a_accel
