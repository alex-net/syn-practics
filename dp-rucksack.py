from random import randint
from prettytable import PrettyTable
from copy import deepcopy
# задача о рюкзаке ..
# форммируем список вещей для укладывания в рюкзак с их весом от 1 до 20 и ценностью  от 1 до 1000
#
capacity = randint(7, 20)

items = []
for _ in range(randint(5, 11)):
    items.append({
        'w': randint(1, capacity), # вес
        'c': randint(1, 1000) # ценность
    })
items = sorted(items, key= lambda a: a['w'])


class ItemList:
    ''' класс рюкзака '''
    def __init__(self):
        self.__l = set() # предметы в рюкзаке


    def __repr__(self):
        if len(self.__l):
            return '+'.join([str(el+1) for el in self.__l]) + f'({self.weight}/{self.cost})'
        return '-'


    def add(self, i):
        ''' добавление нового элемента '''
        if type(i) is int:
            self.__l.add(i)

        if type(i) is set:
            self.__l |= i

    @property
    def cost(self):
        ''' общая стоимость '''
        return sum([items[el]['c'] for el in self.__l])

    @property
    def weight(self):
        ''' общий вес предметов в рюкзаке '''
        return sum([items[el]['w'] for el in self.__l])

    @property
    def items(self):
        ''' набор элементов '''
        return self.__l


print(f'Вместимость рюкзака (W) {capacity} кг')

print('Предлагаемый набор вещей:')
t = PrettyTable()
t.field_names = ['№', 'Вес, кг', 'Стоимость, р']
for i, r in enumerate(items):
    t.add_row([i + 1, r['w'], r['c']])
print(t)


# Заполнение таблицы нулями .. для всех возможных весов рюкзака и всех вариантов товара
dp = [[ItemList() for __ in range(len(items))] for _ in range(capacity + 1)]

# идём последовательно по весам рюкзака и заполняем ценами на элементы, которые туда влезут
for w in range(1, capacity + 1):
    for i, item in enumerate(items):
        dp[w][i] = deepcopy(dp[w - 1][i])
        if w < item['w']: # вещь не влезла в рюкзак с грузоподъёмностью w
            continue

        if w >= item['w']:
            dp[w][i].add(i)

            if w - dp[w][i].weight > 0:
                fromRow = sorted(dp[w - dp[w][i].weight],  key= lambda it: it.cost)
                dp[w][i].add(fromRow[-1].items)


print('Таблица подбора:')
t = PrettyTable()
t.field_names = ['w'] + list(range(1, len(items) + 1))
for w, r in enumerate(dp):
    t.add_row([w] + r)
print(t)

opt = sorted(dp[-1], key= lambda el: el.cost)

print('Оптимальный вариант заполнени: ', opt[-1])