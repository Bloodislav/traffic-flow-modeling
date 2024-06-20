from abc import ABC

# TODO DTO


class CarInterface(ABC):
    def __init__(self) -> None:
        self.length: float = 4.0
        self.angle: int = 0

        self.a_accceler: float = 2
        self.b_accceler: float = 2

        self.speed_stop: float = 0.5
        self.prev_speed_x: float = 0
        self.prev_speed_y: float = 0

        self.speed_x: float = 0
        self.speed_y: float = 0

        self.a_x: float = 0
        self.a_y: float = 0

    def accelerate() -> None: ...

    def move() -> None: ...


class Car(CarInterface):
    def __init__(self, x: int, y: int, max_speed: float, koeff: float) -> None:
        super().__init__()
        """Инициализация машины."""
        self.a_accceler: float = 2.5
        self.b_accceler: float = 2.5

        self.x: int = x
        self.y: int = y
        self.koeff: float = koeff
        self.max_speed_x: float = max_speed
        self.max_speed_y: float = max_speed / 5

    # ---=== Another ===--- #
    # ! Don't test
    def turn(self, angle_change: float) -> None:
        """Поворот машины на заданный угол."""
        if angle_change >= 0:
            self.angle = min(self.angle + angle_change, 30)
        else:
            self.angle = max(self.angle + angle_change, -30)

    def stop(self) -> None:
        self.stop_x()
        self.stop_y()

    # ---=== Accelerate | Speed ===--- #
    def accelerate_func(
        self, acceleration: float, prev_sped: float, max_speed: float
    ) -> float:
        res: float = acceleration * (1 - (prev_sped / max_speed) ** self.koeff)
        return res.real

    def _deceleration(self, speed: float) -> None:
        # TODO
        accel: float = -self.speed_stop if self.speed_x > 0 else self.speed_stop

    # ------ Cord X ------ #
    def accelerate_x(self, acceleration: float) -> None:
        self.a_x = self.accelerate_func(
            acceleration, self.prev_speed_x, self.max_speed_x
        )

    def stop_x(self) -> None:
        self.speed_x, self.a_x = [0, 0]

    def _speed_x_limit(self, speed: float, max_speed: float) -> float:
        result: float = (
            min(speed.real, max_speed)
            if speed.real >= 0
            else max(speed.real, -max_speed / 3)
        )
        return result

    def _deceleration_x(self) -> None:
        accel: float = -self.speed_stop if self.speed_x > 0 else self.speed_stop
        self.accelerate_x(accel)
        self.speed_x += self.a_x

    # ------ Cord Y ------ #
    def accelerate_y(self, acceleration: float) -> None:
        self.a_y = self.accelerate_func(
            acceleration, self.prev_speed_y, self.max_speed_y
        )

    def stop_y(self) -> None:
        self.speed_y, self.a_y = [0, 0]

    def _speed_y_limit(self, speed: float, max_speed: float) -> float:
        result: float = (
            min(speed.real, max_speed)
            if speed.real >= 0
            else max(speed.real, -max_speed)
        )
        return result

    def _deceleration_y(self) -> None:
        accel: float = -self.speed_stop if self.speed_y > 0 else self.speed_stop
        self.accelerate_y(accel)
        self.speed_y += self.a_y

    # ---=== Move | Update ===--- #
    def move(self) -> None:
        """Обмновление скорости"""
        self.prev_speed_x = self.speed_x
        self.speed_x += self.a_x
        self.speed_x = self._speed_x_limit(self.speed_x, self.max_speed_x)

        self.prev_speed_y = self.speed_y
        self.speed_y += self.a_y
        self.speed_y = self._speed_y_limit(self.speed_y, self.max_speed_y)

    def update(self) -> None:
        """Обновление позиции авто."""
        self.move()

        self.x += int(self.speed_x.real)
        self.y += int(self.speed_y.real)

        # Сброс скорости
        self._deceleration_x() if abs(self.speed_x) > self.speed_stop else self.stop_x()
        self._deceleration_y() if abs(self.speed_y) > self.speed_stop else self.stop_y()
