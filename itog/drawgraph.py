import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
from math import sqrt
import calcs


class DrawGraph(tk.Frame):
    ''' виджет для отображения и опитимизации графа .. '''
    TYPE_SHOW_DIMENSIONS = {
        'len': 'Расстояние',
        'time': 'Время',
        'cost': 'Стоисость'
    }
    ALGOS = {
        'afu' : 'Флойда-Уоршелла',
        'dijkstra' : 'Дейкстры',
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args,**kwargs)
        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=0, weight=1)

        # используемый алгоритм оптимизации
        self.__calc = None
        self.__optimalPath = None

        conrols = tk.Frame(self);
        tk.Label(conrols, text='Настройки:').pack()
        tk.Label(conrols, text='Величина').pack()
        vals = list(DrawGraph.TYPE_SHOW_DIMENSIONS.values())
        self.__typeDataShow = ttk.Combobox(conrols, values=vals, state='readonly' )
        self.__typeDataShow.pack()
        self.__typeDataShow.set(vals[0])
        self.__typeDataShow.bind('<<ComboboxSelected>>', self.__draw)

        tk.Label(conrols, text='Алгоритм').pack()
        vals = list(DrawGraph.ALGOS.values())
        self.__algo = ttk.Combobox(conrols, values=vals, state='readonly' )
        self.__algo.pack()
        self.__algo.set(vals[0])
        self.__algo.bind('<<ComboboxSelected>>', self.__draw)

        tk.Label(conrols, text='Из точки').pack()
        self.__from = ttk.Combobox(conrols, values=[], state='readonly' )
        self.__from.bind('<<ComboboxSelected>>', self.__draw)
        self.__from.pack()
        tk.Label(conrols, text='В точку').pack()
        self.__to = ttk.Combobox(conrols, values=[], state='readonly' )
        self.__to.bind('<<ComboboxSelected>>', self.__draw)
        self.__to.pack()

        tk.Button(conrols, text='Перерисовать', command=self.__draw).pack(side=tk.BOTTOM)
        conrols.grid(row=0, column=0, sticky='nws')

        fig = Figure(figsize=(16, 16), dpi=100, layout="compressed")

        self.__ax = fig.add_subplot(frame_on=False)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=0, column=1, sticky='nswe')

        self.__canvasDrawCB = canvas.draw

        self.__draw();

        self.bind('<<refresh-draws>>', self.__refresAll)

    @property
    def __optimalNodes(self):
        ''' вернуть оптимальные вершины из оптимального маршрута '''
        optimalApexes = [];
        if self.__calc:
            for p in self.__calc.optimalPath:
                optimalApexes.extend(p)
        optimalApexes = set(optimalApexes)
        return optimalApexes


    def __refresAll(self, e):
        ''' данные графа изменились - надо обновить все списки '''

        comboData = [f'#{el["iid"]} {el["name"]}' for el in self.master.dataPanels.get('Apex').userData ]
        self.__from.configure(values=comboData)
        self.__from.set('')
        self.__to.configure(values=comboData)
        self.__to.set('')
        # убить текущий расчёт (пусть пересчитывает заново )
        self.__calc = None
        # оптимальный маршрут сотоит из вершин
        self.__optimalPath = []

        self.__draw()


    def __getEndVal(self, pathEl, apexes):
        ''' генерим данные для веса рёбер '''
        return {
            'len': int(sqrt((apexes[pathEl['from']]['cx']-apexes[pathEl['to']]['cx'])**2 + (apexes[pathEl['from']]['cy']-apexes[pathEl['to']]['cy'])**2)),
            'time': pathEl['time'],
            'cost': pathEl['cost']
        }


    @property
    def __dimensionType(self):
        ''' ключ оптимизируемой величины '''
        return list(DrawGraph.TYPE_SHOW_DIMENSIONS.keys())[self.__typeDataShow.current()];


    def __draw(self, e=None):
        ''' перерисовка крафа '''

        # граф ...)
        gr = nx.DiGraph(directed=True)

        # Наборы даных графа (вершины и рёбра )
        graphData = {k:w.userData for k,w in  self.master.dataPanels.items()}

        # отдельный набор вершин ...
        apexDict = {el['iid']:el for el in graphData['Apex']}

        gr.add_nodes_from([el['iid'] for el in apexDict.values()])

        # добавление рёбер с подписями ..
        gr.add_edges_from([(el['from'], el['to'], self.__getEndVal(el, apexDict)) for el in graphData['Edge']])

        # чё-то поменяли в настройках
        if e and isinstance(e.widget, ttk.Combobox):
            self.__optimalPath = []
            # поменялась оптимизируемая величина / алгоритм оптимизации
            if e.widget in (self.__typeDataShow, self.__algo):
                self.__calc = None

        # используемый алгоритм оптимизации
        algo = list(DrawGraph.ALGOS.keys())[self.__algo.current()]
        algo = algo.title().replace('-', '')
        if self.__calc is None and hasattr(calcs, algo):
            self.__calc = getattr(calcs, algo)(gr, self.__dimensionType)

        points = {k: getattr(self, '_DrawGraph__' + k).current() for k in ('from', 'to')}
        if points['from'] != -1  and points['from'] != points['to'] and not self.__optimalPath:
            if hasattr(self.__calc, 'calcAllPathsFrom'): # для Дейкстры обстываем расстояния для начальной точки
                self.__calc.calcAllPathsFrom(points['from'])
            if points['to'] != -1:
                self.__optimalPath = self.__calc.optimalPath(points['from'], points['to'])

        self.__ax.clear()

        # оптимальный путь из наборов рёбер между оптимальными верщинами
        optimalPathEdges = []
        if self.__optimalPath:
            for a in range(len(self.__optimalPath) - 1):
                optimalPathEdges.append((self.__optimalPath[a], self.__optimalPath[a+1]))

        pos = nx.spring_layout(gr)
        nx.draw_networkx_nodes(gr, pos, node_color=['red' if self.__optimalPath and noda in self.__optimalPath else 'gray' for noda in gr.nodes()] , node_size=500, ax=self.__ax)
        nx.draw_networkx_edges(gr, pos, edge_color=['red' if (u,v) in optimalPathEdges else "grey" for u, v, d in gr.edges(data=True)], ax=self.__ax)
        nx.draw_networkx_labels(gr, pos, font_size=12, font_family="sans-serif", ax=self.__ax)
        nx.draw_networkx_edge_labels(gr, pos, edge_labels={(u, v): d[self.__dimensionType] for u, v, d in gr.edges(data=True)}, ax=self.__ax)

        self.__canvasDrawCB()
