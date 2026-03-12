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
    bounds = [0, None, len(arr)-1]

    while True:
        bounds[1] = (bounds[2] + bounds[0]) // 2
        # нашелся элемент - возвращаем индекс
        if arr[bounds[1]] == sVal:
            return bounds[1]

        # Выход по совпадению (смыканию) границ поиска
        if bounds[0] == bounds[2]:
            return -1

        if arr[bounds[1]] > sVal:
            bounds[2] = bounds[1]
        else:
            bounds[0] = bounds[1] + 1


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
