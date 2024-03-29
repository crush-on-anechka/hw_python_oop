from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import ClassVar, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    M_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_RUN_1: ClassVar[float] = 18
    COEFF_CALORIE_RUN_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
                          (self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                           - self.COEFF_CALORIE_RUN_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.M_IN_H
        )
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    COEFF_CALORIE_WLK_1: ClassVar[float] = 0.035
    COEFF_CALORIE_WLK_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
                          (self.COEFF_CALORIE_WLK_1 * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * self.COEFF_CALORIE_WLK_2 * self.weight)
            * self.duration * self.M_IN_H
        )
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int

    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_SWM_1: ClassVar[float] = 1.1
    COEFF_CALORIE_SWM_2: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
                          (self.get_mean_speed() + self.COEFF_CALORIE_SWM_1)
            * self.COEFF_CALORIE_SWM_2 * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    match: dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    try:
        return match[workout_type](*data)
    except KeyError:
        print(f'Некорректное значение кода тренировки - {workout_type}')
        raise


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
