class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOURS_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        new_message = InfoMessage(self.__class__.__name__,
                                  self.duration, self.get_distance(),
                                  self.get_mean_speed(),
                                  self.get_spent_calories()
                                  )
        return new_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.HOURS_IN_MIN
                    )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    SECOND_CALORIES_WEIGHT_MULTIPLIER = 0.029
    KMPERH_IN_MPERS = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.HOURS_IN_MIN
        mean_speed_in_m_per_sec = self.get_mean_speed() * self.KMPERH_IN_MPERS
        height_in_m = self.height / self.CM_IN_M
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    + (mean_speed_in_m_per_sec**2 / height_in_m)
                    * self.SECOND_CALORIES_WEIGHT_MULTIPLIER * self.weight)
                    * duration_in_min
                    )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_TERM = 1.1
    CALORIES_MULTIPLIER = 2

    def __init__(self, action: int,
                 duration: int,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_TERM)
                    * self.CALORIES_MULTIPLIER * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_codes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return type_codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
