class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:

        self.training_type = training_type
        self.duration = (duration)
        self.distance = (distance)
        self.speed = (speed)
        self.calories = (calories)

    def get_message(self) -> str:  # вывод сообщения на консоль
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65   # один шаг в м
    M_IN_KM: int = 1000   # kонстанта для перевода  из метров в километры.
    MIN_IN_H: int = 60   # константа для перевода часы в минуты
    CM_IN_M: float = 100  # константа для перевода  см. в мет.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action   # действие
        self.duration = duration   # продолжительность
        self.weight = weight   # вес

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message1 = InfoMessage(self.__class__.__name__,
                               self.duration,
                               self.get_distance(),
                               self.get_mean_speed(),
                               self.get_spent_calories())
        return message1


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, weight: float, duration: float) -> None:
        super().__init__(action, weight, duration)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float  # Рост спортсмена
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278  # перевод КМ в Метрах в секунду

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                 ** 2 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))
    # Перерасчет калорий для спортивной ходьбы


class Swimming(Training):
    """Тренировка: плавание."""

    count_pool: int  # сколько раз пользователь переплыл бассейн.
    length_pool: int  # длина бассейна в метрах
    LEN_STEP: float = 1.38  # перераспределение константы из шага в гребок
    SWIMING_CONST_1: float = 1.1
    SWIMING_CONST_2: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        action = count_pool * length_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

        #  Формула расчёта средней скорости при плавании

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.SWIMING_CONST_1) * self.SWIMING_CONST_2 * self.weight * self.duration

        # Формула для расчёта израсходованных калорий


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }  # словарь, инициализированный парами имя=значение
    if read.get(workout_type) is None:
        return None
    readdat = read.get(workout_type)(*data)
    return readdat


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
