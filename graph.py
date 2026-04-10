from prettytable import PrettyTable, TableStyle
import json

class DirectedGraph:
    ''' класс ориентированного графа ..'''

    def __init__(self, file=None):
        ''' Инициирование элементов графа из файла '''
        self.__vertexes = [] # Набор вершин
        self.__edges = [] # набор рёбер

        if file is None:
            return

        try:
            json.load(open(file), object_pairs_hook=self._dataDocoder)
        except OSError as e:
            print('Не могу прочитать файл', file)
        except json.JSONDecodeError as e:
            print('Ошибка в формате', e)


    def _dataDocoder(self, data = None):
        ''' обработка данных файла для импорта '''
        for v, t in data:
            if type(t) is str:
                t = [t]
            for el in t:
                self.add_edge(v, el)


    def add_vertex(self, name):
        ''' добавиление вершин
            name - Наименование вершины
        '''
        if name in self.__vertexes:
            print(f'Вершина "{name}" уже добавлена')
            return
        self.__vertexes.append(name)



    def add_edge(self, f, t):
        ''' добавление рёбер
            f - начальная вершина ребра (источник)
            t - конечная вершина ребра (приёмник)
        '''
        if f == t:
            print(f'"{f}" -> "{t}" не является ребром' )
            return
        # Добавляем вершины, которых нет в списке
        for r in [f, t]:
            if r not in self.__vertexes:
                self.add_vertex(r)

        edge = (f, t)
        if edge in self.__edges:
            print(f'Ребро "{f}" -> "{t}" уже добавлено в граф')
            return
        self.__edges.append(edge)

    def __repr__(self):
        ''' крткое отображение графа '''
        return f'Граф состоит из {len(self.__vertexes)} вершин и {len(self.__edges)} рёбер'
    def detail(self):
        ''' детальная информация о графе '''
        print(f'Вершины ({len(self.__vertexes)}):', ', '.join(self.__vertexes))
        print(f'Рёбра: ({len(self.__edges)})', ', '.join('->'.join(el) for el in self.__edges))

    def dfs(self, vertex=None, init=True):
        ''' обход в ширину
            vertex - начальная вершина обхода
        '''
        fn = self.__class__.dfs
        # инициирование переменных
        if not hasattr(fn, 'vs') or init:
            fn.vs = [] # место сбора вершин обхода
            fn.que = [] # очередь обхода вершин
            if vertex is None:
                raise ValueError('Не задана начальная вершина обхода графа')
            if not vertex in self.__vertexes:
                raise ValueError(f'У графа не вершины {vertex}')

        if vertex:
            fn.que.append(vertex)
        ql = len(fn.que)
        for i in range(ql): # для каждого узла в очереди
            v = fn.que.pop(0)
            if v in fn.vs: # вершина уже пройдена ..
                continue
            fn.vs.append(v)
            for f, t in self.__edges:
                if v == f: # если нашли ребро начинащееся с этой вершины - доюавляем в очередь вершину на втором конце ребра
                    fn.que.append(t)

        if len(fn.que):
            self.dfs(init=False)
        if init:
            return fn.vs

    def contiguityMatrix(self):
        ''' матрица смежности '''
        if not self.__vertexes:
            print('нечего выводить')
            return
        table = PrettyTable()
        table.field_names = [''] + self.__vertexes
        for r in self.__vertexes:
            table.add_row([r] + ['1' if (r, el) in self.__edges else '0' for el in self.__vertexes]) # [1] * len(self.__vertexes)
        print(table)

    def contiguityList(self):
        ''' список смежности '''
        if not self.__vertexes:
            print('нечего выводить')
            return
        table = PrettyTable()
        table.field_names = ['Вершина', 'Смежные вешины']
        table.align['Смежные вешины'] = 'l'
        for r in self.__vertexes:
            binds = [t for (f, t) in self.__edges if f == r ]
            if binds:
                table.add_row([r, ', '.join(binds)])
        print(table)



dg = DirectedGraph()
dg.add_vertex('das')
dg.add_vertex('das11')

dg.add_edge('ds', '3341')
dg.add_edge('ds', '3343')
dg.add_edge('ds', '3344')
dg.add_edge('ds', '3345')
dg.add_edge('das', 'ds')
dg.add_edge('ds', 'ds')
dg.add_edge('3344', 'das11')
dg.add_edge('das11', 'das154')
dg.add_edge('3344', 'ds')

print(dg)
dg.detail()
for v in ['das', 'das11']:
    print(f'Обход по вершине {v}', dg.dfs(v))

dg.contiguityMatrix()
dg.contiguityList()


dg2 = DirectedGraph('graph-matrix.json')
dg2.contiguityMatrix()

dg3 = DirectedGraph('graph-list.json')
dg3.contiguityMatrix()

