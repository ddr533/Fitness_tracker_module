import re
import pytest
import types
import inspect
from conftest import Capturing

try:
    import fitnes_tracker
except ModuleNotFoundError:
    assert False, 'Не найден файл с домашней работой `fitnes_tracker.py`'
except NameError as exc:
    name = re.findall("name '(\w+)' is not defined", str(exc))[0]
    assert False, f'Класс {name} не обнаружен в файле домашней работы.'
except ImportError:
    assert False, 'Не найден файл с домашней работой `fitnes_tracker.py`'


def test_read_package():
    assert hasattr(fitnes_tracker, 'read_package'), (
        'Создайте функцию для обработки '
        'входящего пакета - `read_package`'
    )
    assert callable(fitnes_tracker.read_package), (
        '`read_package` должна быть функцией.'
    )
    assert isinstance(fitnes_tracker.read_package, types.FunctionType), (
        '`read_package` должна быть функцией.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (('SWM', [720, 1, 80, 25, 40]), 'Swimming'),
    (('RUN', [15000, 1, 75]), 'Running'),
    (('WLK', [9000, 1, 75, 180]), 'SportsWalking'),
])
def test_read_package_return(input_data, expected):
    result = fitnes_tracker.read_package(*input_data)
    assert result.__class__.__name__ == expected, (
        'Функция `read_package` должна возвращать класс '
        'вида спорта в зависимости от кода тренировки.'
    )


def test_InfoMessage():
    assert inspect.isclass(fitnes_tracker.InfoMessage), (
        '`InfoMessage` должен быть классом.'
    )
    info_message = fitnes_tracker.InfoMessage
    info_message_signature = inspect.signature(info_message)
    info_message_signature_list = list(info_message_signature.parameters)
    for p in ['training_type', 'duration', 'distance', 'speed', 'calories']:
        assert p in info_message_signature_list, (
            'У метода `__init__` класса `InfoMessage` должен быть '
            f'параметр {p}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    (['Swimming', 1, 75, 1, 80],
        'Тип тренировки: Swimming; '
        'Длительность: 1.000 ч.; '
        'Дистанция: 75.000 км; '
        'Ср. скорость: 1.000 км/ч; '
        'Потрачено ккал: 80.000.'
     ),
    (['Running', 4, 20, 4, 20],
        'Тип тренировки: Running; '
        'Длительность: 4.000 ч.; '
        'Дистанция: 20.000 км; '
        'Ср. скорость: 4.000 км/ч; '
        'Потрачено ккал: 20.000.'
     ),
    (['SportsWalking', 12, 6, 12, 6],
        'Тип тренировки: SportsWalking; '
        'Длительность: 12.000 ч.; '
        'Дистанция: 6.000 км; '
        'Ср. скорость: 12.000 км/ч; '
        'Потрачено ккал: 6.000.'
     ),
])
def test_InfoMessage_get_message(input_data, expected):
    info_message = fitnes_tracker.InfoMessage(*input_data)
    assert hasattr(info_message, 'get_message'), (
        'Создайте метод `get_message` в классе `InfoMessage`.'
    )
    assert callable(info_message.get_message), (
        '`get_message` в классе `InfoMessage` должен быть методом.'
    )
    result = info_message.get_message()
    assert isinstance(result, str), (
        'Метод `get_message` в классе `InfoMessage`'
        'должен возвращать значение типа `str`'
    )
    assert result == expected, (
        'Метод `get_message` класса `InfoMessage` должен возвращать строку.\n'
        'Например: \n'
        'Тип тренировки: Swimming; '
        'Длительность: 1.000 ч.; '
        'Дистанция: 75.000 км; '
        'Ср. скорость: 1.000 км/ч; '
        'Потрачено ккал: 80.000.'
    )


def test_Training():
    assert inspect.isclass(fitnes_tracker.Training), (
        '`Training` должен быть классом.'
    )
    for attr, value in {
            'LEN_STEP': 0.65,
            'M_IN_KM': 1000,
            'MIN_IN_H': 60
    }.items():
        assert hasattr(fitnes_tracker.Training, attr), (
            f'У класса `Training` должна быть константа `{attr}`'
        )
        assert getattr(fitnes_tracker.Training, attr) == value, (
            'У класса `Training` должна быть '
            f'константа `{attr}` со значением `{value}`'
        )
    training = fitnes_tracker.Training
    training_signature = inspect.signature(training)
    training_signature_list = list(training_signature.parameters)
    for param in ['action', 'duration', 'weight']:
        assert param in training_signature_list, (
            'У метода `__init__` класса `Training` должен быть '
            f' параметр {param}.'
        )
    assert 'LEN_STEP' in list(training.__dict__), (
        'Задайте константу `LEN_STEP` в классе `Training`'
    )
    assert training.LEN_STEP == 0.65, (
        'Длина шага в классе `Training` должна быть равна 0.65'
    )
    assert 'M_IN_KM' in list(training.__dict__), (
        'Задайте константу `M_IN_KM` в классе `Training`'
    )
    assert training.M_IN_KM == 1000, (
        'В классе `Training` укажите правильное '
        'количество метров в километре: 1000'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.273),
    ([1206, 12, 6], 0.7838999999999999),
])
def test_Training_get_distance(input_data, expected):
    training = fitnes_tracker.Training(*input_data)
    assert hasattr(training, 'get_distance'), (
        'Создайте метод `get_distance` в классе `Training`.'
    )
    result = training.get_distance()
    assert type(result) == float, (
        'Метод `get_distance` в классе `Trainig`'
        'должен возвращать значение типа `float`'
    )
    assert result == expected, (
        'Проверьте формулу подсчета дистанции класса `Training`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.06825),
    ([1206, 12, 6], 0.065325),
])
def test_Training_get_mean_speed(input_data, expected):
    training = fitnes_tracker.Training(*input_data)
    assert hasattr(training, 'get_mean_speed'), (
        'Создайте метод `get_mean_speed` в классе `Training`.'
    )
    result = training.get_mean_speed()
    assert type(result) == float, (
        'Метод `get_mean_speed` в классе `Training`'
        'должен возвращать значение типа `float`'
    )
    assert result == expected, (
        'Проверьте формулу подсчета средней скорости движения '
        'класса `Training`'
    )


@pytest.mark.parametrize('input_data', [
    ([9000, 1, 75]),
    ([420, 4, 20]),
    ([1206, 12, 6]),
])
def test_Training_get_spent_calories(input_data):
    training = fitnes_tracker.Training(*input_data)
    assert hasattr(training, 'get_spent_calories'), (
        'Создайте метод `get_spent_calories` в классе `Training`.'
    )
    assert callable(training.get_spent_calories), (
        '`get_spent_calories` должна быть функцией.'
    )


def test_Training_show_training_info(monkeypatch):
    training = fitnes_tracker.Training(*[720, 1, 80])
    assert hasattr(training, 'show_training_info'), (
        'Создайте метод `show_training_info` в классе `Training`.'
    )

    def mock_get_spent_calories():
        return 100
    monkeypatch.setattr(
        training,
        'get_spent_calories',
        mock_get_spent_calories
    )
    result = training.show_training_info()
    assert result.__class__.__name__ == 'InfoMessage', (
        'Метод `show_training_info` класса `Training` '
        'должен возвращать объект класса `InfoMessage`.'
    )


def test_Swimming():
    assert hasattr(fitnes_tracker, 'Swimming'), 'Создайте класс `Swimming`'
    assert inspect.isclass(fitnes_tracker.Swimming), (
        '`Swimming` должен быть классом.'
    )
    assert issubclass(fitnes_tracker.Swimming, fitnes_tracker.Training), (
        'Класс `Swimming` должен наследоваться от класса `Training`.'
    )
    Swimming_attr_values = fitnes_tracker.Swimming.__dict__.values()
    for _, value in {
            'CALORIES_MEAN_SPEED_SHIFT': 1.1,
            'CALORIES_WEIGHT_MULTIPLIER': 2,
    }.items():
        assert value in Swimming_attr_values, (
            'У класса `Swimming` должна быть '
            f'константа со значением `{value}`'
        )

    swimming = fitnes_tracker.Swimming
    swimming_signature = inspect.signature(swimming)
    swimming_signature_list = list(swimming_signature.parameters)
    for param in ['action', 'duration', 'weight', 'length_pool', 'count_pool']:
        assert param in swimming_signature_list, (
            'У метода `__init__` класса `Swimming` '
            f' должен быть параметр {param}.'
        )
    assert 'LEN_STEP' in list(swimming.__dict__), (
        'Задайте константу `LEN_STEP` в классе `Swimming`'
    )
    assert swimming.LEN_STEP == 1.38, (
        'Длина гребка в классе `Swimming` должна быть равна 1.38'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 1.0),
    ([420, 4, 20, 42, 4], 0.042),
    ([1206, 12, 6, 12, 6], 0.005999999999999999),
])
def test_Swimming_get_mean(input_data, expected):
    swimming = fitnes_tracker.Swimming(*input_data)
    result = swimming.get_mean_speed()
    assert result == expected, (
        'Переопределите метод `get_mean_speed` в классе `Swimming`. '
        'Проверьте формулу подсчёта средней скорости в классе `Swimming`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 336.0),
    ([420, 4, 20, 42, 4], 182.72),
    ([1206, 12, 6, 12, 6], 159.264),
])
def test_Swimming_get_spent_calories(input_data, expected):
    swimming = fitnes_tracker.Swimming(*input_data)
    result = round(swimming.get_spent_calories(), 3)
    assert type(result) == float, (
        'Переопределите метод `get_spent_calories` в классе `Swimming`.'
    )
    assert result == expected, (
        'Проверьте формулу расчёта потраченных калорий в классе `Swimming`'
    )


def test_SportsWalking():
    assert hasattr(fitnes_tracker, 'SportsWalking'), 'Создайте класс `SportsWalking`'
    assert inspect.isclass(fitnes_tracker.SportsWalking), (
        '`SportsWalking` должен быть классом.'
    )
    assert issubclass(fitnes_tracker.SportsWalking, fitnes_tracker.Training), (
        'Класс `SportsWalking` должен наследоваться от класса `Training`.'
    )
    for attr, value in {
            'CALORIES_WEIGHT_MULTIPLIER': 0.035,
            'CALORIES_SPEED_HEIGHT_MULTIPLIER': 0.029,
            'KMH_IN_MSEC': 0.278,
            'CM_IN_M': 100
    }.items():
        assert hasattr(fitnes_tracker.SportsWalking, attr), (
            f'У класса `SportsWalking` должна быть константа `{attr}`'
        )
        assert round(getattr(fitnes_tracker.SportsWalking, attr), 3) == value, (
            'У класса `SportsWalking` дожна быть '
            f'константа `{attr}` со значением `{value}`'
        )
    sports_walking = fitnes_tracker.SportsWalking
    sports_walking_signature = inspect.signature(sports_walking)
    sports_walking_signature_list = list(sports_walking_signature.parameters)
    for param in ['action', 'duration', 'weight', 'height']:
        assert param in sports_walking_signature_list, (
            'У метода `__init__` класса `SportsWalking` '
            f'должен быть параметр {param}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75, 180], 349.252),
    ([420, 4, 20, 42], 168.119),
    ([1206, 12, 6, 12], 151.544),
])
def test_SportsWalking_get_spent_calories(input_data, expected):
    sports_walking = fitnes_tracker.SportsWalking(*input_data)
    result = round(sports_walking.get_spent_calories(), 3)
    assert type(result) == float, (
        'Переопределите метод `get_spent_calories` в классе `SportsWalking`.'
    )
    assert result == expected, (
        'Проверьте формулу подсчёта потраченных '
        'калорий в классе `SportsWalking`'
    )


def test_Running():
    assert hasattr(fitnes_tracker, 'Running'), 'Создайте класс `Running`'
    assert inspect.isclass(fitnes_tracker.Running), '`Running` должен быть классом.'
    assert issubclass(fitnes_tracker.Running, fitnes_tracker.Training), (
        'Класс `Running` должен наследоваться от класса `Training`.'
    )
    Running_attr_values = fitnes_tracker.Running.__dict__.values()
    for _, value in {
            'CALORIES_MEAN_SPEED_MULTIPLIER': 18,
            'CALORIES_MEAN_SPEED_SHIFT': 1.79
    }.items():
        assert value in Running_attr_values, (
            'У класса `Running` должна быть '
            f'константа со значением `{value}`'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 481.905),
    ([420, 4, 20], 14.489),
    ([1206, 12, 6], 12.812),
])
def test_Running_get_spent_calories(input_data, expected):
    running = fitnes_tracker.Running(*input_data)
    assert hasattr(running, 'get_spent_calories'), (
        'Создайте метод `get_spent_calories` в классе `Running`.'
    )
    result = round(running.get_spent_calories(), 3)
    assert type(result) == float, (
        'Переопределите метод `get_spent_calories` в классе `Running`.'
    )
    assert result == expected, (
        'Проверьте формулу расчёта потраченных калорий в классе `Running`'
    )


def test_main():
    assert hasattr(fitnes_tracker, 'main'), (
        'Создайте главную функцию программы с именем `main`.'
    )
    assert callable(fitnes_tracker.main), '`main` должна быть функцией.'
    assert isinstance(fitnes_tracker.main, types.FunctionType), (
        '`main` должна быть функцией.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (['SWM', [720, 1, 80, 25, 40]], [
        'Тип тренировки: Swimming; '
        'Длительность: 1.000 ч.; '
        'Дистанция: 0.994 км; '
        'Ср. скорость: 1.000 км/ч; '
        'Потрачено ккал: 336.000.'
    ]),
    (['RUN', [1206, 12, 6]], [
        'Тип тренировки: Running; '
        'Длительность: 12.000 ч.; '
        'Дистанция: 0.784 км; '
        'Ср. скорость: 0.065 км/ч; '
        'Потрачено ккал: 12.812.'
    ]),
    (['WLK', [9000, 1, 75, 180]], [
        'Тип тренировки: SportsWalking; '
        'Длительность: 1.000 ч.; '
        'Дистанция: 5.850 км; '
        'Ср. скорость: 5.850 км/ч; '
        'Потрачено ккал: 349.252.'
    ]),
    (['WLK', [9000, 1.5, 75, 180]], [
        'Тип тренировки: SportsWalking; '
        'Длительность: 1.500 ч.; '
        'Дистанция: 5.850 км; '
        'Ср. скорость: 3.900 км/ч; '
        'Потрачено ккал: 364.084.'
    ]),
    (['WLK', [3000.33, 2.512, 75.8, 180.1]], [
        'Тип тренировки: SportsWalking; '
        'Длительность: 2.512 ч.; '
        'Дистанция: 1.950 км; '
        'Ср. скорость: 0.776 км/ч; '
        'Потрачено ккал: 408.429.'
    ]),
])
def test_main_output(input_data, expected):
    with Capturing() as get_message_output:
        training = fitnes_tracker.read_package(*input_data)
        fitnes_tracker.main(training)
    assert get_message_output == expected, (
        'Метод `main` должен печатать результат в консоль.\n'
    )
