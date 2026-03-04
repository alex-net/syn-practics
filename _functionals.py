import sqlite3 as sql
import os
from prettytable import PrettyTable
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from password_generator import gen as passGenFunc
from usage_monitor import LoggerDecor

class App:
    def __init__(self):
        # чтение .env файла
        load_dotenv()
        # соединение с базой
        self.__dbCon = None

        cryptoKey = os.getenv('cryptoKey', None)
        try:
            if cryptoKey is None:
                raise ValueError('пустое значение')
            # нужен для шифрования расшифрования паролей ..
            self.__encryptor = Fernet(cryptoKey)
        except ValueError:
            print(f'Поместите значение "{Fernet.generate_key().decode()}" в значение ключа "cryptoKey" .env файла')
            return

        # Инициируем базу ..
        dbFileName = os.getenv('dbFile', 'pm.db')
        self.__dbCon = sql.connect(dbFileName)
        # проверяем права доступа к файлу .. Если надо меняем на 600
        if f'{os.stat(dbFileName).st_mode:o}'[-3:] != '600':
            os.chmod(dbFileName, 0o600)

        curs = self.__dbCon.cursor()
        curs.execute('create table if not exists pm (login text primary key, password text)')
        self.__dbCon.commit();
        curs.close()

        while True:
            cmd = input('Введите команду (add,list,get,del): ').strip()
            match cmd:
                case 'add':
                    if self.__addOper():
                        print('Данные добавлены')
                case 'del':
                    if self.__delOper():
                        print('Данные удалены')
                case 'get':
                    loginData = self.__getOper()
                    if loginData:
                        print(f'Логин: "{loginData[0]}"; пароль: "{loginData[1]}"')
                    else:
                        print('Данные не нашлись..')
                case 'list':
                    self.__listOper()
                case _:
                    return

    def __del__(self):
        ''' Завершение приложения'''
        if isinstance(self.__dbCon, sql.Connection):
            self.__dbCon.close()


    def __getLogin(self):
        ''' запрос логина ...'''
        login = input('Введите логин: ').strip()
        # ввели пустой логин ...  либо проверка не нужна
        if not login:
            return (login, False,)

        curs = self.__dbCon.cursor()
        curs.execute('select count(*) from pm where login = ?', (login,))
        res = curs.fetchone()
        curs.close()
        return (login, res[0] > 0, )

    @property
    def getDbCon(self):
        ''' вернуть подключение к базе ..'''
        return self.__dbCon

    @LoggerDecor
    def __addOper(self):
        ''' добавление пары логин/пароль '''
        # запрос логина
        loginData = self.__getLogin()
        if not loginData[0]:
            print(f'Логин "{loginData[0]}" пуст... ')
            return False
        if loginData[1]:
            print(f'Логин "{loginData[0]}" уже занят..')
            return False

        # С логином всё ОК, запрашиваем пароль ...
        pas = input('Введите пароль либо 1 - для генерации слабого пароля, 2 - сложного пароля: ').strip()
        match pas:
            case '1':
                pas = passGenFunc()
            case '2':
                pas = passGenFunc('complex')

        if not pas and  input('Пароль пуст.. Продолжить (+/-)? ').strip() != '+':
            return False

        # Шифруем ....
        pas = self.__encryptor.encrypt(pas.encode())

        # сохранение данных
        curs = self.__dbCon.cursor()
        curs.execute('insert into pm (login, password) values (?, ?)', (loginData[0], pas))
        self.__dbCon.commit();
        curs.close()
        return True


    @LoggerDecor
    def __delOper(self):
        ''' Удаление записи '''
        loginData = self.__getLogin()
        if not loginData[0] or not loginData[1]:
            print('нечего удалять...')
            return False

        # Удаление записи
        curs = self.__dbCon.cursor()
        curs.execute('delete from pm where login = ?', (loginData[0],))
        self.__dbCon.commit();
        curs.close()
        return True


    @LoggerDecor
    def __getOper(self):
        ''' запрос данных по логину ..'''
        loginData = self.__getLogin()
        # Данные есть в базе
        if not loginData[1]:
            return False

        curs = self.__dbCon.cursor()
        curs.execute('select * from pm where login = ?', (loginData[0],))
        row = list(curs.fetchone())
        curs.close()
        row[1] = self.__encryptor.decrypt(row[1]).decode();
        return row


    def __listOper(self):
        ''' просмотр списка базы паролей ..'''
        tbl = PrettyTable()
        tbl.title = 'Данные сервисов'
        tbl.field_names = ['Логин', 'Пароль']
        curs = self.__dbCon.cursor()
        curs.execute('select * from pm ')
        while True:
            row = curs.fetchone()
            if not row:
                break
            row = list(row)
            row[1] = self.__encryptor.decrypt(row[1]).decode();
            tbl.add_row(row)
        curs.close()
        print(tbl)













