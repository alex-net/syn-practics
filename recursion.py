from math import factorial
from random import shuffle, randint
from funcs import Sequence

print('Факториал числа N')
def myFactorial(n:int) -> int:
    '''' факториал числа n '''
    return n * myFactorial(n - 1) if n > 1 else 1

# делаем выборку значений для вычисления факториала ...
l = list(range(1, 11))
shuffle(l)
for n in l[:4]:
    print(f'{n}! = {factorial(n)} = {myFactorial(n)}')


print('Вычисление суммы ')
def allSumm(l:list = []) -> int:
    ''' вычисление суммы всех лементов .. '''
    return l[0] + (0 if len(l) == 1 else allSumm(l[1:]))

l = list(range(1, 1000))
for i in range(4):
    shuffle(l)
    ln = l[:10]
    print(f'{chr(425)}{ln} = {sum(ln)} = {allSumm(ln)}')

print('Биинареый поиск')
def binSearchRecurs(v:int, arr:list = [], f:int = 0, t:int = None) -> int:
    ''' бинартный поиск на рекурсии '''
    t = len(arr) if t is None else t
    # условие выхода - массив закончился и совпадений нет ...
    if t - f < 2 and arr[f] != v:
        return -1
    midl = (t + f) // 2
    if arr[midl] == v:
        return midl
    return binSearchRecurs(v, arr, f, midl) if arr[midl] > v else binSearchRecurs(v, arr, midl+1, t)

shuffle(l)
r = l[10:15]
l = list(range(1, 1000))
for n in r:
    print('число', n, 'индекс1 =', l.index(n), 'индекс2 =', binSearchRecurs(n, l))


# Напишите класс Stack, который реализует основные операции стека: push, pop, is_empty и peek
print('класс Stack')
class Stack(Sequence):
    ''' класс стека '''
    def push(self, v:int) -> None:
        ''' положить в стек '''
        self._data.append(v)

    def pop(self) -> int:
        ''' вынуть из стека '''
        return None if not len(self._data) else self._data.pop()

    def  __repr__(self):
        return f'Стек <{len(self._data)}> head: {self.peek()},{' не ' if not self.is_empty() else ' '}пустой'

stack = Stack()
print(stack)

for i in range(3):
    n = randint(-100, 1000)
    print('Кладём в стек', n)
    stack.push(n)

print(stack)
print('Забрали значение ', stack.pop())
for i in range(3):
    print('Забрали значение ', stack.pop())
    print(stack)
