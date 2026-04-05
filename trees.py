from treeart import binary_edge
from random import randint

# http://shtanyuk.ru/edu/nntu/ads/pdf/lec11.pdf
# https://habr.com/ru/articles/267855/
# операции над элементами бинатрного дерева
#

class BinaryTree:
    _left = None # левая ветка
    _right = None # правая ветка
    _data = None # данные
    __searchLevel = 0


    def insert(self, data):
        ''' Вставка новых данных в дерево '''
        # проверяем текущее значенике узла ..
        if self._data is None:
            self._data = data
            return
        # значение меньше текущего узла добавляются в левую ветку
        if self._data > data:
            if self._left is None:
                self._left = self.__class__()
            self._left.insert(data)
        # значение большее текущего узла добавляются в правую ветку
        if self._data < data:
            if self._right is None:
                self._right = self.__class__()
            self._right.insert(data)

    @property
    def val(self):
        ''' вернуть данные '''
        return self._data

    @property
    def l(self):
        ''' левое поддерево '''
        return self._left

    @property
    def r(self):
        ''' правое поддерево '''
        return self._right

    def search(self, val):
        ''' поиск элемента в дереве ..'''
        self.__class__.__searchLevel += 1
        s = [self._data]
        if self._data > val and self._left:
            s.extend(self._left.search(val))
        if self._data < val and self._right:
            s.extend(self._right.search(val))

        self.__class__.__searchLevel -= 1
        # вышли на корневой элемент ..
        if self.__class__.__searchLevel == 0:
            return  '->'.join([str(el) for el in s]) if val in s else None
        return s

    def __repr__(self):
        ''' построение дерева '''
        if self._left or self._right:
            return binary_edge(self._data, self._left, self._right)
        return str(self._data)



class AVLTree(BinaryTree):
    ''' бинарное дерево с балансировкой '''
    @property
    def height(self):
        ''' высота дерева '''
        return max(0 if self._left is None else self._left.height, 0 if self._right is None else self._right.height) + 1

    @property
    def isDisbalansed(self):
        leftH = 0 if self._left is None else self._left.height
        rightH = 0 if self._right is None else self._right.height
        return abs(leftH - rightH) > 1

    def insert(self, data):
        ''' вставка элемента с балансировкой '''
        super().insert(data)
        self.reposition()

    def __reorder(self, el1=None, el2=None):
        ''' перегруппировка дерева  '''
        el1 = self if el1 is None else el1
        el2 = self if el2 is None else el2
        subTrees = [el1._left, el2._left, el1._right, el2._right]
        el1, el2 = el2, el1
        el1._data, el2._data = el2._data, el1._data
        el1._left = subTrees[0]
        el1._right = subTrees[1]
        el2._left = subTrees[2]
        el2._right = subTrees[3]


    def reposition(self):
        ''' Определение элемента для перестановки  '''
        if not self.isDisbalansed:
            return
        hl = 0 if self._left is None else self._left.height
        hr = 0 if self._right is None else self._right.height

        if hr < hl: # замена корня на левое поддерево
            self.__reorder(el1=self._left)
        else: # замена корня на правое поддерево
            self.__reorder(el2=self._right)


def roundDepth(tree, type):
    ''' обход в глубину
        tree - корень дерева
        type - очерёдность обхода узлов  l - левыйь, r - правый, v - Значение узла
    '''
    if not hasattr(roundDepth, 'level'):
        roundDepth.level = 0

    if not roundDepth.level:
        roundDepth.buff = []


    roundDepth.level += 1
    for item in type:

        if item == 'v':
            roundDepth.buff.append(tree.val)
        if hasattr(tree, item) and getattr(tree, item):
            roundDepth(getattr(tree, item), type)

    roundDepth.level -=1
    if not roundDepth.level:
        return roundDepth.buff




def roundWidth(tree = None):
    ''' обход дерева в ширину '''
    # очередь обхода дерева и буфер возврата
    if tree:
        roundWidth.level = 0 # уровень вложенности вызовов
        roundWidth.que = [tree] # очередь обхода элементов уровня
        roundWidth.buff = [] # результат работы функции

    if not roundWidth.que:
        return roundWidth.buff

    # обойти элементы в очереди

    # сколько уже накоплено
    l = len(roundWidth.que)
    for i in range(l):
        el = roundWidth.que.pop(0)

        roundWidth.buff.append(el.val)

        for atr in ['l', 'r']:
            stree = getattr(el, atr)
            if stree:
                roundWidth.que.append(stree)

    if len(roundWidth.que):
        roundWidth()

    return roundWidth.buff


tree = AVLTree()
print('Случайная последовательность')
for i in range(20):
    d = randint(0, 1000)
    tree.insert(d)
    print(d, end=', ')
print()
print(tree)
print('обход дерева в ширину', roundWidth(tree))
print('обход дерева в длину vlr', roundDepth(tree, 'vlr'))
print('обход дерева в длину lrv', roundDepth(tree, 'lrv'))
print('обход дерева в длину lvr', roundDepth(tree, 'lvr'))
print(f'Максимальная глубира {tree.height}, дизбаланс:', 'есть' if tree.isDisbalansed else 'нет' )


tree = AVLTree()
print('Упорядоченная последовательность')
for i in range(20):
    tree.insert(i)
    print(i, end=', ')
print()
print(tree)
print(f'Максимальная глубира {tree.height}, дизбаланс:', 'есть' if tree.isDisbalansed else 'нет' )

for d in [9, 19, 8, 5, 15, 100]:
    print(f'поиск {d}:', tree.search(d))



