import telebot
from telebot.types import BotCommand
from os.path import exists as fileExists
from dbstorage import DbStorage
from os import environ
import readenv.loads
from telebot.apihelper import ApiTelegramException

class TodoListBot(telebot.TeleBot):

    def __init__(self, *args, **kwargs):
        try:
            self.__db = DbStorage()
        except ConnectionError as e:
            print(e)
            return
        tokenApi = environ.get('TG_API_TOKEN')
        if tokenApi is None:
            print('Не указан API-TOKEN для бота')
            return

        super().__init__(tokenApi, *args, **kwargs)

        try:
            self.set_my_commands([
                BotCommand('start', ' — приветственное сообщение.'),
                BotCommand('help', ' — показать список доступных команд.'),
                BotCommand('add', '<название> — добавить новую задачу'),
                BotCommand('list', ' — вывести список текущих задач.'),
                BotCommand('complete', '<номер> — отметить задачу как выполненную.'),
                BotCommand('delete', '<номер> — удалить задачу по номеру.'),
            ])
        except  ApiTelegramException as e:
            print(e)
            return

        # приветствеие ...
        self.send_welcome = (self.message_handler(commands=['start']))(self.send_welcome)

        # сообщение спрвка ...
        self.send_help_message = (self.message_handler(commands=['help']))(self.send_help_message)

        # Добавлени нового задания
        self.add_new_job = (self.message_handler(commands=['add']))(self.add_new_job)
        #  список задачек
        self.add_new_job = (self.message_handler(commands=['list']))(self.list_jobs)
        # выполненная задачка
        self.task_make_complete = (self.message_handler(commands=['complete']))(self.task_make_complete)
        # удаление ...
        self.task_delete = (self.message_handler(commands=['delete']))(self.task_delete)

        # просто сообщения ...
        self.any_message = (self.message_handler(func=lambda message: True))(self.any_message)

        self.infinity_polling()



    def any_message(self, message):
        ''' ругатся по умолчанию .. '''
        self.reply_to(message, 'Что-то пошло не так. Я не знаю такой команды')


    def send_help_message(self, message):
        ''' Справочная функция '''
        cmds = []
        for cmd in self.get_my_commands():
            cmds.append(f'/{cmd.command} {cmd.description}')
        cmds = '\n '.join(cmds)
        self.send_message(message.chat.id, f'Доступные команды\n {cmds}')


    def send_welcome(self, message):
        ''' приветствеие '''
        msg = f'Привет, @{message.from_user.username}!'
        helloFilePath = environ.get('HELLO_MSG_FILE')
        if fileExists(helloFilePath):
            hm = open(helloFilePath)
            msg =  hm.read().format(f'@{message.from_user.username}')
            hm.close()

        self.send_message(message.chat.id, msg)


    def add_new_job(self, message):
        ''' добавление нового задания '''
        # Вытаскиваем названия задания
        jobName = message.text[4:].strip()
        try:
            taskNum = self.__db.addTask(message.from_user.id, jobName)
        except ValueError as e:
            self.reply_to(message, e)
        else:
            self.reply_to(message, f'Задачка успешно добавлена с номером {taskNum}')


    def __taskFormatter(self, mess):
        ''' фрматирование одной задачки '''
        text = f'{mess[0]}\) {mess[2]}'
        if mess[1]:
            text = f'~{text}~'
        return text


    def list_jobs(self, message):
        ''' показать список задач и выйти ..'''
        tasks = self.__db.getTasks(message.from_user.id)
        if tasks:
            tasks = 'Текущие задачки:\n' + '\n'.join(map(self.__taskFormatter, tasks))
        else:
            tasks = 'Задачки не найдены'

        self.send_message(message.chat.id, tasks, parse_mode='MarkdownV2')


    def task_make_complete(self, message):
        ''' сделать задачку выполненной '''
        jobInd = message.text[9:].strip()
        try:
            taskTitle = self.__db.setTaskComplete(message.from_user.id, jobInd)
        except ValueError as e:
            self.reply_to(message, e)
        else:
            self.send_message(message.chat.id, f'Задачку "{taskTitle}" отмелили как выполненную')


    def task_delete(self, message):
        ''' удаление '''
        jobInd = message.text[7:].strip()
        try:
            taskTitle = self.__db.killTask(message.from_user.id, jobInd)
        except ValueError as e:
            self.reply_to(message, e)
        else:
            self.send_message(message.chat.id, f'Задачка "{taskTitle}" Удалена.')

# запуск бота ...
if __name__ == '__main__':
    TodoListBot()