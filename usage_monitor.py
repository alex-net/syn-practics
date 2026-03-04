
class LoggerDecor:
    ''' Класс логера '''
    def __init__(self, fn):
        ''' создание объекта логера под каждый метод '''
        self.__fn = fn
        self.__pm = None


    def __get__(self, inst, own):
        ''' запрос созданного объекта логера из объекта менеджера паролей '''
        if not self.__pm:
            self.__pm = inst
            self.__checkTables()
        return self


    def __call__(self, *args, **kvargs):
        ''' вызов подменяемого метода ... '''
        print('call')
        ret = self.__fn(self.__pm, *args, **kvargs)
        if ret:
            self.__logOper(self.__fn.__name__[2:-4], self.__pm.getDbCon)
        return ret


    def __checkTables(self):
        ''' проверка струкруты и строк .. '''
        cursor = self.__pm.getDbCon.cursor()
        # Добавляем таблицу лога ...
        cursor.execute('create table if not exists pm_log (oper text, co integer)')
        # делаем запрос количества записей ..
        cursor.execute('select count(*) from pm_log')
        coRow = cursor.fetchone()
        # записи есть ... нужно выйти ..
        if coRow[0]:
            return
        # собрать данные по операциям ..
        opers = [a[6:-4] for a in dir(self.__pm) if a.endswith('Oper') and callable(getattr(self.__pm, a))]
        # обнуление количества ...
        opers = list(zip(opers, [0] * len(opers)))
        cursor.executemany('insert into pm_log values(?, ?)', opers)
        self.__pm.getDbCon.commit()
        cursor.close()


    def __logOper(self, oper, dbCon):
        ''' логер ..который добавляет единичку .. '''
        curs = dbCon.cursor()
        curs.execute('update pm_log set co = co + 1 where oper = ?', (oper,))
        dbCon.commit()
        curs.close()



# если запустили как самостоятельное приложение .. пробуем посмотреть что насобирали ...
if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    from sys import argv
    import sqlite3 as sql
    from prettytable import PrettyTable

    load_dotenv()
    dbFile = os.getenv('dbFile')
    # файл базы не найден ...
    if not os.path.exists(dbFile):
        print('Не нашли файл базы...')
        exit()
    con = sql.connect(dbFile)
    curs = con.cursor()
    # ищем таблицу ... )
    curs.execute('select count(*) from sqlite_schema where name = "pm_log"')
    tblCo = curs.fetchone()
    try:
        # не нашли таблицу ...
        if tblCo[0] == 0:
            raise SystemExit('не нашли таблицу с логом')

        if len(argv) > 1:
            match argv[1]:
                # зачистка лога..
                case 'clean':
                    curs.execute('update pm_log set co = 0')
                    con.commit()
                    raise SystemExit('Лог очищен')

        tbl = PrettyTable()
        tbl.title = 'Отчёт по действиям'
        tbl.field_names = ['Действие', 'Количество']
        curs.execute('select * from pm_log')
        for row in curs.fetchall():
            tbl.add_row(row)
        print(tbl)

    except SystemExit as e:
        print(e)
    finally:
        curs.close()
        con.close()
