import threading

import telebot

import test_bd

bot = telebot.TeleBot('1641457298:AAEXwjDb83msBchf8e7UxPLYCvBq8tG-Uec')
bot.send_message(392812944, 'Запуск')  # отправка сообщения по id пользователя

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Курлык')

dataReg = []
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Зарегистрироваться', 'Авторизироваться', 'Гость')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


done = False
messagel = []


@bot.message_handler(content_types=['text'])
def send_text(message):
    messagel.append(str(message.text))
    print(messagel)
    # if message.text == 'Курлык':
    #     bot.send_message(message.chat.id, 'Хы, курлык')
    # elif message.text == 'Пока':
    #     bot.send_message(message.chat.id, 'Не курлык')
    # elif message.text == 'Гыг':
    #     bot.send_message(message.chat.id, 'Гыгык')
    # elif message.text == 'Привет':
    #     bot.send_message(message.chat.id, 'Хы')
    # elif message.text == 'Уйди':
    #     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMlYE9lizdxS_7RVlla7BVA5LBHXvcAArsAA_cCyA9kl0GTZTAcwB4E')
    # elif message.text == 'Милый котик':
    #     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMzYE9pEfdhse-QG1icaeF0xRSlYIwAArgAAzDUnRH3ZYYNzwzrFR4E')
    if message.text == 'курлык':
        bot.send_message(message.chat.id, 'привет')
    elif message.text == 'Гость':
        bot.send_message(message.chat.id, 'Хы')
    elif message.text == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свою фамилию: ')
        register(messagel, message)
    elif messagel[len(messagel) - 2] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свое имя: ')
        register(messagel, message)
    elif messagel[len(messagel) - 3] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свое отчество: ')
        register(messagel, message)
    elif messagel[len(messagel) - 4] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свою должность (1 - управляющая, 0 - нет): ')
        register(messagel, message)
    elif messagel[len(messagel) - 5] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите id своего департамента (2 - Маркетинг, 3 - Работа с клиентами, '
                                          '4 - Закупки): ')
        register(messagel, message)
    elif messagel[len(messagel) - 6] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свой email: ')
        register(messagel, message)
    elif messagel[len(messagel) - 7] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свой телефонный номер: ')
        register(messagel, message)
    elif messagel[len(messagel) - 8] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите пароль: ')
        print(message.from_user.id)
        register(messagel, message)
    elif message.text == 'Авторизироваться':
        bot.send_message(message.chat.id, 'Хы')
    else:
        register(messagel, message)


def register(messagel, message):
    if 'Зарегистрироваться' in messagel:
        if messagel[len(messagel) - 1] != 'Зарегистрироваться':
            dataReg.append(messagel[len(messagel) - 1])
    else:
        print('Нажато не то')
    if len(dataReg) == 8:
        print('Вызвалась')
        dataReg.append(message.from_user.id)
        test_bd.insData(test_bd.tableName, test_bd.tableColumns, dataReg)
        dataReg.clear()
    print('dataReg', dataReg)
    return dataReg


# отправка сообщения по конкреному id
def sendMes(id, text):
    bot.send_message(id, text)


file_names = ['2021-04-23t17-30-43.txt']  # создаем массив, в котором будут храниться названия текущего и предыдущего


# файлов


def sendWarning(userId):
    file = test_bd.getScripts(test_bd.engine_testBD)
    print(file.name)
    # test_bd.compareDiff('2021-04-23t9-11-21.txt', file.name)
    # test_bd.compareDiff('2021-04-23t17-30-43.txt', file.name)
    test_bd.compareDiff(file_names[0], file.name)
    file_names.append(file.name)
    if len(file_names) != 0:
        del file_names[0]
    data_file = []  # сюда попадают все данные из файла изменений
    send_add = []  # сюда отфильтровываются только данные по добавлению
    send_del = []  # сюда отфильтровываются только данные по удалению
    send_change = []  # сюда отфильтровываются только данные по изменению
    with open('file3.txt', "r") as fin:
        www = fin.read()
        for string in www.split('\n'):
            data_file.append(string)

    for item in data_file:
        if '^' in item and '?' in item:  # фильтр по изменению
            send_change.append(item)
        elif '+' in item and '^' not in item:  # фильтр по добавлению
            send_add.append(item)
        elif '-' in item and '^' not in item:  # фильтр по удалению
            send_del.append(item)

    if len(send_change) != 0:
        send_change.insert(0, 'Произошло изменение в следующих строках: ')
        for item in send_change:
            sendMes(userId, item)
    if len(send_add) != 0:
        send_add.insert(0, 'Произошло добавление следующих строк: ')
        for item in send_add:
            sendMes(392812944, item)
    if len(send_del) != 0:
        send_del.insert(0, 'Произошло удаление следующих строк: ')
        for item in send_del:
            sendMes(392812944, item)

    # threading.Timer(600, sendWarning()).start()


def call_repeatedly(interval, func, *args):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)

    threading.Thread(target=loop).start()
    return stopped.set


userId = 392812944
call_repeatedly(60, sendWarning, userId)

# @bot.message_handler(content_types=['text'])
# def send_text(message):
#   print(message)
# @bot.message_handler(content_types=['sticker'])
# def send_text(message):
#     print(message)
#
#
# @bot.message_handler(content_types=['photo'])
# def send_text(message):
#     print(message)


bot.polling()
# server = 'IRNEF\SQLEXPRESS'
# database = 'BMS'
# tableName = 'Users'
# tableColumns = ' (surName, name, midName, isHead, departmentId, email, phoneNumber, pass) '
# test_bd.insData(tableName, tableColumns, dataReg)
