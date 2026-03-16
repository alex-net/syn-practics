import funcs, types
from prettytable import PrettyTable, TableStyle

@funcs.DeTimeDecorator
def bibbleSort(arr):
    ''' сортировка пузырьком '''
    while True:
        applyed = False
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                applyed = True
        if not applyed:
            break
    return arr

@funcs.DeTimeDecorator
def selectionSort(arr):
    ''' сортировка выбором '''
    for it in range(len(arr)):
        minI = it
        # поиск минимального значения
        for i in range(it, len(arr)):
            if arr[minI] > arr[i]:
                minI = i
        if it != minI:
            arr[minI], arr[it] = arr[it], arr[minI]
    return arr

@funcs.DeTimeDecorator
def insertSort(arr):
    ''' сортировка вставками '''
    for it in range(len(arr) - 1):
        if arr[it] <= arr[it + 1]:
            continue

        el = arr[it + 1]
        for i in range(it + 1, 0, -1):
            arr[i] = arr[i - 1]
            if el > arr[i]:
                arr[i] = el
                break
        else:
            arr[0] = el

    return arr

@funcs.DeTimeDecorator
def mergeSort(arr):
    ''' сортировка слянием '''
    # для массива c длиной менее 2 элементов ничего не делаем ...
    if len(arr) < 2:
        return None

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    mergeSort(left_half)
    mergeSort(right_half)
    i = j = k = 0
    # Слияние двух половин
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
             arr[k] = right_half[j]
             j += 1
        k += 1

    # Проверка остатков
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1
    return arr


sorted = funcs.DeTimeDecorator(sorted)

# for n in [1000, 100, 10]:
rows = {}
headers = ['*', 10, 100, 1000]
for n in headers[1:]:
    arr = funcs.rangeGen(n)[0]

    for (name, fn,) in [
        ('пузырёк', bibbleSort),
        ('выбор', selectionSort),
        ('вставки', insertSort),
        ('слияние', mergeSort),
        ('build-in', sorted)
    ]:
        nArr = fn(arr.copy())
        if name not in rows:
            rows[name] = []

        rows[name].append(fn.dt)
        # rows.append([name, ])
        # print(f'{name} ({n})',  f'dt={}нс' )

table = PrettyTable()
print('Зависимость производительности разных типов сортировок от длины входных данных')

table.field_names = [n if n == '*' else f'{n} шт' for n in headers]
table.add_rows([[name] + [f'{el:>,d} нс' for el in data] for (name, data) in rows.items()])
table.align = dict(zip(table.field_names, ['l']+['r']*(len(table.field_names)-1)))
table.set_style(TableStyle.MARKDOWN)
print(table)