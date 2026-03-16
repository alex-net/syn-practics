from random import randint

class HashTable:
    def __init__(self, size):
        ''' инициализация хеш-таблицы '''
        self.__size = size
        self.__table = [[] for _ in range(size)]

    def _hash_function(self, key):
        ''' Вычисление индекса в хеш таблице '''
        # Для ключей строк - считаем сумму кодов символов строки ..
        if isinstance(key, str):
            return sum([ord(c) for c in key]) % self.__size
        # для всего остального - делаем как раньше ..
        return hash(key) % self.__size

    def insert(self, key, value):
        ''' добавление элемента '''
        index = self._hash_function(key)
        for pair in self.__table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.__table[index].append([key, value])

    def search(self, key):
        ''' поиск элемента в хештаблице '''
        index = self._hash_function(key)
        for pair in self.__table[index]:
            if pair[0] == key:
                return pair[1]

    def delete(self, key):
        ''' удаление элемента '''
        index = self._hash_function(key)
        for i, pair in enumerate(self.__table[index]):
            if pair[0] == key:
                del self.__table[index][i]

    def resize(self, size):
        ''' изменение размера.'''
        # Резмер меняется только в большую сторону. в противном случае будет потеря данных
        if size > self.__size:
            self.__table.extend([[] for _ in range(size - self.__size)] )
        if size < self.__size: # обрезка таблицы  по новому размеру ...
            self.__table = self.__table[:size]
        self.__size = size

    @property
    def size(self):
        ''' вернуть длину хеш таблицы '''
        return len(self.__table)

    @property
    def used(self):
        ''' вернуть словарь с занятостью ключей таблицы'''
        used = {}
        for (ind, val) in enumerate(self.__table):
            if len(val):
                used[ind] = len(val)
        return used


# Пример использования:
ht = HashTable(5)
ht.insert("name", "Alice")
print(ht.search("name"), end='\n\n') # Вывод: Alice
ht.delete("name")
print(ht.search("name"), end='\n\n') # Вывод: None

print('размер', ht.size, end='\n\n')
ht.resize(10)
print('размер', ht.size, end='\n\n')

keys = []
print('Кладём в таблицу 25 значений', end='\n\n')
for x in range(25):
    r = randint(0,100)
    keys.append(f"{x}name-{r}")
    ht.insert(keys[-1] , f"Alice-{x}-{r}")

# print(ht.size)
print('Использование хеш-таблицы', ht.used, end='\n\n')
print('Созданные ключи', keys, end='\n\n')
print(f'ключ "{keys[14]}"; значение "{ht.search(keys[14])}"', end='\n\n')
