import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from types import MappingProxyType

class FucPlus:
    @property
    def widgetType(self):
        cls = self.__class__.__name__
        for k in ('Panel', 'Dialog'):
           cls = cls.replace(k, '')
        return cls

    def getApexList(self):
        ''' вернуть список точек (вешин) в виде словаря '''
        comboList = dict()
        # путь до ближайшей панели
        panelW = self if self is AppPanel else self.nametowidget(self.winfo_parent())
        for w in panelW.winfo_toplevel().winfo_children():
            if 'ApexPanel' == w.__class__.__name__:
                for el in w.userData:
                    comboList[el["iid"]] = f'#{el["iid"]} {el["name"]} ({el["cx"]}, {el["cy"]})'
        return comboList


class AppBaseDialog(tk.Toplevel, FucPlus):
    DLG_CLASS = 'AppDialog'
    ''' базовый класс диалогового окна '''
    def __init__(self, master, data=dict(),  *args, **kwargs):

        kwargs['class_'] = AppBaseDialog.DLG_CLASS

        super().__init__(master, *args, **kwargs)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        # print('dataWin', self.__dataWin)

        # self.event_generate('<<test-event>>', data=['wwqeeqw'])
        # сохранить ссылку на родительское окно
        self.__dataWin = data
        self._initForm()
        tk.Button(self, text='Отмена', command= lambda: self.destroy()).grid(row=100, column=0)
        tk.Button(self, text='Применить', command= self._applyForm).grid(row=100, column=1)

        self.wait_visibility()
        self.grab_set()
        self.transient(master)

    def _initForm(self):
        ''' инициализация формы '''
        pass
    def _applyForm(self):
        ''' применение формы = Тыкнули на применить'''
        pass

    def _dataReady(self, data):
        self.__dataWin |= data
        self.event_generate('<<event-data-ready>>')

    @property
    def userData(self):
        ''' вернуть данные из формы '''
        return self.__dataWin


class ApexDialog(AppBaseDialog):
    ''' добавление/редактирование вершин '''
    FIELDS = MappingProxyType({'name': 'Наименование', 'cx': 'Координата X', 'cy': 'Координата Y'})

    def _initForm(self):
        ''' накручиваем элементы формв '''

        self.title('Редактирование вершины' if len(self.userData) else 'Добавление вершины');

        tk.Label(self, text='Наименование').grid(row=0, column=0, columnspan=2)
        self.__name = tk.Entry(self)
        if self.userData and 'name' in self.userData:
            self.__name.insert(0, self.userData['name'])
        self.__name.grid(row=1, column=0, columnspan=2, sticky='ew')
        for i, k in enumerate(('cx', 'cy')):
            tk.Label(self, text=self.FIELDS[k]).grid(row=2, column=i)
            el = tk.Entry(self)
            if self.userData and k in self.userData:
                el.insert(0, self.userData[k])
            el.grid(row=3, column=i, sticky='ew')
            setattr(self, '_' + self.__class__.__name__ + '__'+k, el)



    def _applyForm(self):
        data = dict()
        try:
            el = None
            data['name'] = self.__name.get()
            if not len(data['name']):
                self.__name.focus()
                raise ValueError('Название вершины не должно быть пустым')

            for k in ('cx', 'cy'):
                el = getattr(self, '_' + self.__class__.__name__ + '__' + k)
                data[k] = int(el.get())
        except ValueError as e:
            if el:
                el.focus()
            showerror('Ошибка!', e, parent=self)
        else:
            self._dataReady(data)
            self.destroy()


class EdgeDialog(AppBaseDialog):
    ''' диалоговое окно добавления ребра '''

    FIELDS = MappingProxyType({'from': 'Из точки', 'to': 'В точку', 'time': 'Время (ч.)', 'cost': 'Стоимость (р.)'})
    def _initForm(self):
        self.title('Редактирование пути' if len(self.userData) else 'Добавление пути');

        # comboList = dict()
        comboList = self.getApexList()

        tk.Label(self, text=self.FIELDS['from']+':', anchor='e').grid(column=0, row=0, sticky='ew')
        self._w_from = ttk.Combobox(self, values=list(comboList.values()), exportselection=0, state='readonly')
        val = self.userData.get('from', '')
        if val in comboList:
            self._w_from.set(comboList[val])
        self._w_from.grid(column=1, row=0, sticky='ew')

        tk.Label(self, text=self.FIELDS['to']+':', anchor='e').grid(column=0, row=1, sticky='ew')
        self._w_to = ttk.Combobox(self, values=list(comboList.values()), exportselection=0, state='readonly')
        val = self.userData.get('to', '')
        if val in comboList:
            self._w_to.set(comboList[val])
        self._w_to.grid(column=1, row=1, sticky='ew')

        tk.Label(self, text=self.FIELDS['time']+':', anchor='e').grid(column=0, row=2, sticky='ew')
        self._w_time = tk.Entry(self, )
        self._w_time.insert(0, self.userData.get('time', ''))
        self._w_time.grid(column=1, row=2, sticky='ew')
        tk.Label(self, text=self.FIELDS['cost']+':', anchor='e').grid(column=0, row=3, sticky='ew')
        self._w_cost = tk.Entry(self, )
        self._w_cost.insert(0, self.userData.get('cost', ''))
        self._w_cost.grid(column=1, row=3, sticky='ew')

    def _applyForm(self):
        data = dict()
        try:
            for a in self.FIELDS:
                w = getattr(self, '_w_' + a)
                val = w.get().strip()
                if not val:
                    raise ValueError(f'Поле "{self.FIELDS[a]}" не должно быть пустым')
                if isinstance(w,ttk.Combobox): # обработка точек ..
                    val = val.split(maxsplit=1)
                    val = val[0][1:]
                elif not val.isdecimal() or int(val) <= 0:
                    raise ValueError(f'Значение поля "{self.FIELDS[a]}" должно быть положительным числовым')
                else:
                    val = int(val)
                data[a] = val
            if data['from'] == data['to']:
                raise ValueError('Пункты должны быть разными')

            for path in self.nametowidget(self.winfo_parent()).userData:
                if path['from'] == data['from'] and path['to'] == data['to'] and path['iid'] != self.userData.get('iid', None):
                    raise ValueError('Путь уже добвлен')

        except ValueError as e:
            w.focus()
            showerror('Ошибка!', e, parent=self)
        else:
            self._dataReady(data)
            self.destroy()



class AppPanel(tk.Frame, FucPlus):
    ''' базовый класс панели '''
    panelTitle = None # наименование панели
    def  __init__(self, *args, **kwargs):
        self.__dataList = []
        super().__init__(*args, **kwargs)

        self._dlgClass = globals()[self.widgetType+'Dialog'];

        topW = self.winfo_toplevel()
        self.__menu = tk.Menu(topW.mainMenu, tearoff=0)

        topW.mainMenu.add_cascade(label=self.panelTitle, menu=self.__menu)
        self.__menu.add_command(label='Добавить', command=lambda: self._dlgClass(self, dict()))
        self.__menu.add_command(label='Удалить', command=self.__removeData, state=tk.DISABLED)

        # fram = tk.Frame(self)
        tk.Label(self, text=self.panelTitle).pack(fill=tk.X)
        # .pack(side=tk.LEFT, expand=1)
        # fram.

        fields = fields = vars(self._dlgClass)['FIELDS']
        self._tree = ttk.Treeview(self, columns=tuple(fields.keys()), show="headings")
        for key, title in fields.items():
            self._tree.heading(key, text=title)
            self._tree.column(key, stretch=True)
        self._tree.pack(fill=tk.BOTH, expand=1)
        # выделение элемента для удаления
        self._tree.bind('<<TreeviewSelect>>', self.__treeSel)
        # редактирование элемента
        self._tree.bind('<Double-Button-1>', self.__treeItemEdit)
        self.bind_class(AppBaseDialog.DLG_CLASS, '<<event-data-ready>>', self.__updateData, add='+')

    def __treeSel(self, e):
        ''' управление выдлением/невыделением в treeView '''
        self.__menu.entryconfigure(1, state= tk.ACTIVE if len(e.widget.selection()) else tk.DISABLED)
        # self.__killBtn.configure)

    def __removeData(self):
        ''' удаление данных из списка '''
        treeSel = self._tree.selection()
        self.__dataList = list(filter(lambda el: el['iid'] not in treeSel,  self.__dataList))
        self._tree.delete(*treeSel)
        # пиннуть панель  с путями - чтобы почистить пути от удалённых точек
        self.master.dataPanels['Edge'].event_generate('<<update-paths>>')
        self.event_generate('<<data-list-changed>>')


    def __treeItemEdit(self, e):
        ''' редактироание .всплыть формой. '''
        sel = e.widget.selection()
        if not len(sel):
            return
        data = list(filter(lambda el: el['iid'] == sel[0], self.__dataList))
        if not data:
            return
        self._dlgClass(self, data[0])


    def __updateData(self, e):
        ''' обработчки передачи данных из диалогового окна '''
        if self.widgetType != e.widget.widgetType:
            return
        data = e.widget.userData
        if 'iid' in data: # обнова элемента
            for i, el in enumerate(self.__dataList):
                if el['iid'] == data['iid']:
                    self.__dataList[i] |= data
            iid = data['iid']
            forTreeRow = self._dataForTree(data) #dict(data.items())
            self._tree.item(iid, values= forTreeRow)
        else: # новые элемент
            data['iid'] = self._tree.insert('', index='end', values= self._dataForTree(data))
            self.__dataList.append(data)
            self._tree.item(data['iid'], values=self._dataForTree(data))
        self.event_generate('<<data-list-changed>>')

    def _dataForTree(self, data):
        ''' генерация последовательности для вставки в TreeView '''
        els = data.copy()
        if 'iid' in els:
            els.pop('iid')
        return tuple(els.values())

    @property
    def userData(self):
        ''' вернуть данные накопленные в списке  '''
        return self.__dataList

    def setUserData(self, data=list()):
        ''' проброс нового списка даннных '''
        els = self._tree.get_children()
        # удалили все элементы
        self.__dataList = list()
        if els:
            self._tree.delete(*els)

        for el in data:
            self.__dataList.append(el.copy())
            iid = el.get('iid', None)
            self._tree.insert('', index='end', iid=iid, values= self._dataForTree(el))


class ApexPanel(AppPanel):

    def __init__(self, *args, **kwargs):
        self.panelTitle = 'Населённые пункты'
        super().__init__(*args, **kwargs)

    def _dataForTree(self, data):
        els = data.copy()
        if 'iid' in data:
            els['name'] = f'#{els["iid"]} {els["name"]}'
        return super()._dataForTree(els)


class EdgePanel(AppPanel):
    def __init__(self, *args, **kwargs):
        self.panelTitle = 'Дороги'
        super().__init__(*args, **kwargs)
        self.bind('<<update-paths>>', self.__cleanEdges)

    def _dataForTree(self, data):
        ''' подготовка данных к выводу в виджет '''
        lst = self.getApexList()
        els = data.copy()
        # замена отображений точек ..
        for k in ('from', 'to'):
            els[k] = lst[els[k]]

        return super()._dataForTree(els)

    def __cleanEdges(self, e):
        ''' обновление по вершинам  зачистка путей   '''
        apLst = list(self.getApexList().keys())
        newEdges = [ el for el in self.userData if el['from'] in apLst and el['to'] in apLst]
        self.setUserData(newEdges)




