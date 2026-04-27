# https://blog.skillfactory.ru/algoritm-floida-uorshella-chto-eto-i-gde-on-polezen/
#

from prettytable import PrettyTable


INF = float('inf') # нет ребра
# матрица смежности
graph = [
    [0, 4, INF, 5, INF],
    [INF, 0, 1, INF, 6],
    [2, INF, 0, 3, INF],
    [INF, INF, 1, 0, 2],
    [1, INF, INF, 4, 0]
]

def printMatrix(dist):
    ''' печать матрицы смежности '''
    t = PrettyTable()
    t.field_names = [''] + [str(el+1) for el in range(len(dist))]
    for i, r in enumerate(dist, 1):
        t.add_row([i] + [str(el) for el in r]);
    print(t)


# Вывод: [0, 2, 5, 1]
# https://habr.com/ru/articles/105825/
#
def afu(dist):
    '''
    dist = матрица расстояний, изначально заполненная весами ребер (или бесконечностью, если ребра нет)
    '''
    for k in range(len(dist)): # номер итерации (перебираем вершины для вставки между двумя сосендями)
        for i in range(len(dist)): # вершина источник
            for j in range(len(dist)):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

printMatrix(graph)
printMatrix(afu(graph))
