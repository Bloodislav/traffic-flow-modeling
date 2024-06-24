from models.car import Car


# # ----=== Speed ===--- #
# def test_move_1(car_object: Car, a_accel: int):
#     car_object.accelerate_x(a_accel)
#     car_object.move()

#     assert car_object.speed_x == a_accel


# def test_move_2(car_object: Car, a_accel: int):
#     car_object.accelerate_y(a_accel)
#     car_object.move()

#     assert car_object.speed_y == a_accel


# def test_move_3(car_object: Car, a_accel: int):
#     car_object.accelerate_y(a_accel)
#     car_object.accelerate_x(a_accel)
#     car_object.move()

#     assert car_object.speed_y == a_accel
#     assert car_object.speed_x == a_accel


# def test_move_4(car_object: Car, a_accel: int):
#     car_object.accelerate_y(-a_accel)
#     car_object.accelerate_x(-a_accel)

#     car_object.move()

#     assert car_object.speed_y == -a_accel
#     assert car_object.speed_x == -a_accel
