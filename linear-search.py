import random
from time import monotonic_ns

dt = None

def dTime(fn):
    def wrap(*args, **kwargs):
        global dt
        t1 = monotonic_ns()
        ret = fn(*args, **kwargs)
        t2 = monotonic_ns()
        dt = t2 - t1
        return ret
    return wrap


@dTime
def linSearch(sVal, arr = []):
    ''' реализация линейного поиска
        :param sVal: элемеент для поиска в массиве arr
        :param arr: линейный массив с элементами
    '''
    for (i,v) in enumerate(arr):
        if v == sVal:
            return i
    return -1

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

for n in [1000, 100, 10]:
    (arr, x, y) = rangeGen(n)
    print('\nРазмер списка', len(arr), 'поиск элементов от', x, 'до', y)

    for i in range(5):
        sdig = random.randint(x, y)
        ind = linSearch(sdig, arr)
        print(f'заход {i + 1}: поиск числа {sdig}. Индекс = {ind}', 'dt=', dt)
