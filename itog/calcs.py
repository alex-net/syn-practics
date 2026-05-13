class GraphOptimist:
    ''' базовый класс оптимизацтора '''
    def __init__(self, gr, dim):
        self._apexes = list(gr.nodes())
        self._edges = {(self._apexes.index(edg[0]), self._apexes.index(edg[1])):edg[2][dim] for edg in gr.edges(data=True) }


    def optimalPath(self, a1, a2):
        ''' пернуть оптимальный путь .. из вершины a1 в a2 '''
        path = [a1] + self._optiimum(a1, a2) + [a2]
        return [self._apexes[p] for p in path]


    def _optiimum(self, a1, a2):
        ''' доп точки для оптимизации '''
        return []


class Afu(GraphOptimist):
    ''' оптимизация по Флойду '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__matrix = []
        # заполнение матрицы смежности
        for apIndX in range(len(self._apexes)):
            self.__matrix.append([]) # добавить строку
            for apIndY in range(len(self._apexes)):
                val = 0 if apIndY == apIndX else 'inf'
                point = (apIndX, apIndY)
                if point in self._edges:
                    val = self._edges.get(point)
                self.__matrix[-1].append(float(val))
        # оптимизация ..
        for k in range(len(self.__matrix)): # номер итерации (перебираем вершины для вставки между двумя сосендями)
            for i in range(len(self.__matrix)): # вершина источник
                for j in range(len(self.__matrix)):
                    self.__matrix[i][j] = self.__kLenCheck(i, j, k)


    def __kLenCheck(self, i, j, k):
        ''' оптимизатор одного варианта '''
        vals = []
        between = []

        for x, y in [(i, j), (i, k), (k,j)]:
            vals.append(self.__matrix[x][y] if type(self.__matrix[x][y]) is float else self.__matrix[x][y]['val'])
            between.append([] if type(self.__matrix[x][y]) is float else self.__matrix[x][y]['b'])

        if vals[0] > vals[1] + vals[2]:
            return {'val': vals[1] + vals[2], 'b': between[1] + [k] + between[2]}
        return self.__matrix[i][j]

    def _optiimum(self, a1, a2):
        return [] if type(self.__matrix[a1][a2]) is float else self.__matrix[a1][a2]['b'][:]




class Dijkstra(GraphOptimist):
    ''' оптимизация путей по алгоритму Дейкстры'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # начальная точка рассчёта
        self.__startPoint = None
        # абор расстояний
        self.__dist = dict()

    def calcAllPathsFrom(self, a1):
        ''' пересчёт всех расстояний от точки a1 '''
        if self.__startPoint == a1: # точка уже просчитана
            return
        self.__startPoint = a1
        self.__dist = dict()

        # для обхода графа по ширине из точки a1
        self.___apexQueue = [(self.__startPoint, dict())]
        # обход графа по ширине с вычислением расстояний
        while self.___apexQueue:
            apex, items = self.___apexQueue.pop(0)
            for path, s in self._edges.items():
                if path[0] == apex:
                    if path[1] not in self.__dist or sum(self.__dist[path[1]].values()) > sum(items.values()) + s:
                        self.__dist[path[1]] = items | {path[1]: s}
                    self.___apexQueue.append((path[1], items | {path[1]: s} ))

    def _optiimum(self, a1, a2):
        path = []
        if a2 in self.__dist:
            path = list(self.__dist[a2].keys())
            path.pop()
        return path


