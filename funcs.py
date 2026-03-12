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