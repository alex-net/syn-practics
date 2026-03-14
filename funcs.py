import random
from time import monotonic_ns


class DeTimeDecorator:
    def __init__(self, fn):
        self.__fn = fn
        self.__dt = None

    def __call__(self, *args, **kwargs):
        t1 = monotonic_ns()
        ret = self.__fn(*args, **kwargs)
        t2 = monotonic_ns()
        self.__dt = t2 - t1
        return ret

    @property
    def dt(self):
        return self.__dt



def rangeGen(size = 100):
    ''' генератор последовательности
        :param size: размер последовательности
    '''
    # сгенерили size чисел
    arr = list(range(size))
    # перемешали
    random.shuffle(arr)
    # допуск для поиска
    percent = int(size * 0.1)
    return (arr, -percent, size + percent)


class Sequence:
    ''' базовый класс последовательности '''
    _data = []

    def is_empty(self) -> bool:
        ''' проверить последовательность на пустоту '''
        return len(self._data) == 0

    def peek(self) -> int:
        ''' посмотреть есть ли что доставать '''
        return self._data[-1] if len(self._data) else None

