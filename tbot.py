import telebot
import test_bd
from telebot import types

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
        register(messagel)
    elif messagel[len(messagel) - 2] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свое имя: ')
        register(messagel)
    elif messagel[len(messagel) - 3] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свое отчество: ')
        register(messagel)
    elif messagel[len(messagel) - 4] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свою должность (1 - управляющая, 0 - нет): ')
        register(messagel)
    elif messagel[len(messagel) - 5] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите id своего департамента (2 - Маркетинг, 3 - Работа с клиентами, '
                                          '4 - Закупки): ')
        register(messagel)
    elif messagel[len(messagel) - 6] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свой email: ')
        register(messagel)
    elif messagel[len(messagel) - 7] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите свой телефонный номер: ')
        register(messagel)
    elif messagel[len(messagel) - 8] == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите пароль: ')
        register(messagel)
    elif message.text == 'Авторизироваться':
        bot.send_message(message.chat.id, 'Хы')
    else:
        register(messagel)


def register(messagel):
    if 'Зарегистрироваться' in messagel:
        if messagel[len(messagel) - 1] != 'Зарегистрироваться':
            dataReg.append(messagel[len(messagel) - 1])
    else:
        print('Нажато не то')
    if len(dataReg) == 8:
        print('Вызвалась')
        test_bd.insData(test_bd.tableName, test_bd.tableColumns, dataReg)
    print('dataReg', dataReg)
    return dataReg


# отправка сообщения по конкреному id
def sendMes(id, text):
    bot.send_message(id, text)


def sendWarning():
    file = test_bd.getScripts(test_bd.metadata_testBD, test_bd.engine_testBD)
    print(file.name)
    test_bd.compareDiff('2021-04-23t9-11-21.txt', file.name)
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
            sendMes(392812944, item)
    if len(send_add) != 0:
        send_add.insert(0, 'Произошло добавление следующих строк: ')
        for item in send_add:
            sendMes(392812944, item)
    if len(send_del) != 0:
        send_del.insert(0, 'Произошло удаление следующих строк: ')
        for item in send_del:
            sendMes(392812944, item)


sendWarning()

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
