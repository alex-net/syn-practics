import psycopg as pg
import readenv.loads
from os import environ


# запрос создания таблицы с задачками ...
SQL_TODO_TABLE = ''' create table if not exists todo_list (
    id serial8 primary key,
    usr int4 not null,
    task_index int not null default 1,
    task_complete bool not null default false,
    task_title varchar(200) not null
); '''

# количество задачек в базе по пользователю
SQL_COUNT_TASKS = 'select count(*) from todo_list where usr = %s'
# добавление новой задачки
SQL_ADD_TASKS = 'insert into todo_list (usr, task_index, task_title) values (%s, %s, %s)'
# список задачек пользователя
SQL_TASKS_LIST = 'select task_index, task_complete, task_title from todo_list where usr = %s order by task_index asc'
# запрос конкретной задачки .. пользователя ..
SQL_GET_TASK = 'select id, task_title, task_complete from todo_list where usr = %s and task_index = %s'
# сделать задачку выполненной ...
SQL_SET_TASK_COMPLETE = 'update todo_list set task_complete = True where  id = %s'
# удаление записи о задачке ..
SQL_DROP_TASK = 'delete from todo_list where id = %s'

LIST_MESSAGE = 'Воспользуйтесь кмандой /list для уточнения номера'


class DbStorage:
    def __init__(self):
        try:
            self.__dbcon = pg.connect(environ.get('DB_CONNECTION'), autocommit=True)
            self.__cursor = self.__dbcon.cursor()
        except pg.OperationalError as e:
            print(e)
            raise ConnectionError('Ошибка соединения с хранилищем...')

        # созаём нужную таблицу
        self.__cursor.execute(SQL_TODO_TABLE)

    def __del__(self):
        ''' закрываем все соединения ..'''
        if not self.__cursor.closed:
            self.__cursor.close()
        if not self.__dbcon.closed:
            self.__dbcon.close()


    def addTask(self, userId, taskName):
        ''' добавление новой задачки '''
        # проверка длины названия
        if len(taskName) > 200:
            raise ValueError('Слишком длинное название')
        if len(taskName) < 1:
            raise ValueError('Забыли указать название задачи')

        # запрос уже добавленных задачек .. чтоб определиться с номером
        self.__cursor.execute(SQL_COUNT_TASKS, params=(userId,))
        coTasks = self.__cursor.fetchone()[0]
        coTasks += 1
        self.__cursor.execute(SQL_ADD_TASKS, params=(userId, coTasks, taskName))
        return coTasks

    def getTasks(self, userId):
        ''' запрос списка задач '''
        self.__cursor.execute(SQL_TASKS_LIST, params=(userId,))
        tasks = self.__cursor.fetchall()
        return tasks

    def __findTask(self, userId, taskInd):
        ''' поиск задачки '''
        if not len(taskInd):
            raise ValueError('Не указан номер задачи')
        if not taskInd.isdigit():
            raise ValueError(f'Нужно указать номер задачи. \n{LIST_MESSAGE}')

        self.__cursor.execute(SQL_GET_TASK, params=(userId, taskInd))
        task = self.__cursor.fetchone()
        if task is None:
            raise ValueError(f'Задачка с номером "{taskInd}" не найдена \n{LIST_MESSAGE}')
        return task


    def setTaskComplete(self, userId, taskInd):
        ''' сделать задачку неактивной  выполненной'''
        task = self.__findTask(userId, taskInd)
        if task[2]:
            raise ValueError(f'Задачка с неомером "{taskInd}" уже выполнена \n{LIST_MESSAGE}')

        self.__cursor.execute(SQL_SET_TASK_COMPLETE, params=(task[0],))
        return task[1]

    def killTask(self, userId, taskInd):
        ''' удалить задачку '''
        task = self.__findTask(userId, taskInd)
        if not task[2]:
            raise ValueError(f'Задачка с неомером "{taskInd}" ещё не выполнена')

        self.__cursor.execute(SQL_DROP_TASK, params=(task[0],))
        return task[1]
