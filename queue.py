from funcs import Sequence
from random import randint

class Queue(Sequence):
    ''' класс очереди '''
    def  __repr__(self):
        return f'Очередь <{len(self._data)}> head: {self.peek()},{' не ' if not self.is_empty() else ' '}пустая'

    def enqueue(self, val):
        ''' добавление элемента в чередь '''
        self._data = [val] + self._data

    def dequeue(self):
        ''' вынуть из очереди '''
        return None if not len(self._data) else self._data.pop()


queue = Queue()
print(queue)

for i in range(3):
    n = randint(-100, 1000)
    print('Кладём в очередь', n)
    queue.enqueue(n)

print(queue)
print('Забрали значение ', queue.dequeue())
for i in range(3):
    print('Забрали значение ', queue.dequeue())
    print(queue)
