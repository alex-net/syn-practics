import tkinter as tk
from tkinter.messagebox import showinfo as tkShowinfo
from tkinter.messagebox import showerror as tkShowerror
from json.decoder import JSONDecodeError
import json
from tkinter import ttk
import os.path as op

from wins import ApexDialog, AppBaseDialog, ApexPanel, EdgePanel, AppPanel
from drawgraph import DrawGraph


class App(tk.Tk):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x400")
        self.title('Оптимизатор маршрутов')

        self.columnconfigure(index=0, weight=1)
        # self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=2, weight=1)

        self.mainMenu = tk.Menu(self)
        self['menu'] = self.mainMenu
        dataMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label='Данные', menu=dataMenu)
        dataMenu.add_command(label='Новый', command=self.__clearUserData)
        dataMenu.add_separator()
        dataMenu.add_command(label='Загрузить...', command=self.__loadAllData)
        dataMenu.add_command(label='Сохранить...', command=self.__saveAllData)
        dataMenu.add_separator()
        dataMenu.add_command(label='Выход', command=  lambda: self.quit())

        ApexPanel(self).grid(row=0, column=0, sticky='nswe')
        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=1, sticky='nswe', padx=2)
        EdgePanel(self).grid(row=0, column=2, sticky='nswe')
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky='nswe', pady=2)
        self.__drawWidget = DrawGraph(self)
        self.__drawWidget.grid(row=2, column=0, columnspan=3, sticky='nswe')

        # перехват изменений данных в графе
        for p in self.dataPanels.values():
            p.bind('<<data-list-changed>>', lambda e: self.__drawWidget.event_generate('<<refresh-draws>>'))

        self.mainloop()


    @property
    def dataPanels(self):
        ''' собрать и вернуть панели с данными '''
        panels = dict()
        for w in self.winfo_children():
            if isinstance(w, AppPanel):
                key = w.__class__.__name__[:-5]
                panels[key] = w
        return panels


    def __clearUserData(self):
        for w in self.dataPanels.values():
            w.setUserData()
        self.__drawWidget.event_generate('<<refresh-draws>>')

    def __saveAllData(self):
        ''' экспорт данных в json файл'''
        data = {k: w.userData for (k, w) in self.dataPanels.items()}

        destFile = op.join(op.dirname(__file__), op.splitext(op.basename(__file__))[0]+'.data')
        fil = open(destFile, mode='w')
        json.dump(data, fil)
        fil.close()
        tkShowinfo(message='Данные сохранены')

    def __loadAllData(self):
        ''' загрузка данных из файла '''
        fn = op.splitext(op.basename(__file__))[0]+'.data'
        destFile = op.join(op.dirname(__file__), fn)
        try:
            fil = open(destFile, mode='r')
            data = json.load(fil)
            fil.close()

            for (key, w) in self.dataPanels.items():
                if key in data:
                    if not type(data[key]) is list:
                        raise ValueError()
                    w.setUserData(data[key])
            self.__drawWidget.event_generate('<<refresh-draws>>')

        except FileNotFoundError as e:
            tkShowerror(message=f'Файл данных "{fn}" не найден', title='Ошибка')
        except JSONDecodeError, ValueError:
            tkShowerror(message=f'Некорректные данные', title='Ошибка')


App()
