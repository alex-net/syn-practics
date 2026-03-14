
def fibonachi(n:int) -> int:
    ''' опеределение числа Фибоначчи '''
    if n < 3:
        return 1
    return fibonachi(n - 1) + fibonachi(n - 2)

print(fibonachi.__doc__.strip() + ':')
print(fibonachi(5))



def findMaxIndex(arr:list, f:int = None, t:int = None) -> tuple:
    ''' максимум из массива '''
    f = f if f is not None else 0
    t = t if t is not None else len(arr) - 1

    if abs(f - t) == 1:
        return  (arr[f], f,) if arr[f] > arr[t] else (arr[t], t,)
    m = (f + t) // 2
    one = findMaxIndex(arr, f, m)
    two = findMaxIndex(arr, m, t)

    return one if one[0] > two[0] else two


from random import shuffle
l = list(range(1000))
shuffle(l)
print(findMaxIndex.__doc__.strip() + ':')
m = max(l)
print(f'максимум = {m}; index = {l.index(m)}')
print('максимум = {}; index = {}'.format(*findMaxIndex(l)))



def quick_sort(arr):
    ''' Быстрая сортировка '''
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
print(quick_sort.__doc__.strip() + ':')
# Пример использования:
arr = [3, 6, 8, 10, 1, 2, 1]
sorted_arr = quick_sort(arr)
print("Отсортированный массив:", sorted_arr)


from funcs import DeTimeDecorator
quick_sort_dt = DeTimeDecorator(quick_sort)
print('Определение производительности алгоритма быстрой сортировки на разных размерах исходных данных:')
for n in [10, 100, 1000]:
    l = list(range(n))
    shuffle(l)
    quick_sort_dt(l)
    print(f'число элементов = {n}, время выполнения = {quick_sort_dt.dt:,d} нс')