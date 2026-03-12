import random
import funcs


@funcs.DeTimeDecorator
def linSearch(sVal, arr = []):
    ''' реализация линейного поиска O(n)
        :param sVal: элемеент для поиска в массиве arr
        :param arr: линейный массив с элементами
    '''
    for (i,v) in enumerate(arr):
        if v == sVal:
            return i
    return -1

@funcs.DeTimeDecorator
def binSearch(sVal, arr = []):
    ''' реализация бинарного поиска O(log n)
        :param sVal: элемеент для поиска в массиве arr
        :param arr: линейный массив с элементами
    '''

    # начальный индекс
    ind = 0

    while True:
        # Выход по пустому массиву
        if not arr:
            return -1
        mid = len(arr) // 2
        # нашелся элемент - возвращаем индекс
        if arr[mid] == sVal:
            return mid + ind
        if arr[mid] > sVal:
            arr = arr[:mid]
        else:
            arr = arr[mid + 1:]
            ind += mid + 1


for n in [1000, 100, 10]:
    (arr, x, y) = funcs.rangeGen(n)
    for (name, fn,) in [
        ('линейный поиск', linSearch),
        ('бинарный поиск', binSearch)
    ]:
        # для бинарного нужен отсортированный массив
        arr = arr if fn is linSearch else sorted(arr)
        print(f'\n*{name}*', 'Размер списка', len(arr), 'поиск элементов от', x, 'до', y)

        for i in range(5):
            sdig = random.randint(x, y)
            ind = fn(sdig, arr)

            print(f'заход {i + 1}: поиск числа {sdig}. Индекс = {ind}', 'dt=', fn.dt, 'нс')
