import threading

import telebot

import test_bd

import re

bot = telebot.TeleBot('1641457298:AAEXwjDb83msBchf8e7UxPLYCvBq8tG-Uec')
bot.send_message(392812944, 'Запуск')  # отправка сообщения по id пользователя

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Курлык')

dataReg = []
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Зарегистрироваться')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


done = False
messagel = []


@bot.message_handler(content_types=['text'])
def send_text(message):
    global messagel
    try:
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
            test_bd.getData(3)
        elif message.text == 'Гость':
            bot.send_message(message.chat.id, 'Хы')
        elif message.text == 'Зарегистрироваться':
            bot.send_message(message.chat.id, 'Введите свою фамилию: ')
            register(messagel, message)
        # elif message.text == 'Авторизироваться':
        #     bot.send_message(message.chat.id, 'Введите пароль: ')
        # elif messagel[len(messagel) - 2] == 'Авторизироваться':
        #     # проверка пароля
        #     print('Проверка пароля')
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
        else:
            register(messagel, message)
    except IndexError:
        bot.send_message(message.chat.id, 'Ошибка ввода, попробуйте заново')
        messagel = []


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


def sendWarning(tablesDep):
    userId = 392812944
    file = test_bd.getScripts(test_bd.engine_testBD)
    print(file.name)
    with open(file.name, 'r') as f:
        nums = f.read().splitlines()

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

    namesTables = []
    columnsTables = []
    delTable = []
    for i, a in enumerate(data_file):
        if ('^' in a and '?' in a) or ('+' in a and '^' not in a) or ('-' in a and '^' not in a):
            if 'Имя таблицы:' in a:
                if '- Имя таблицы: ' in a:
                    m = re.match('.\s*(\w+) (\w+): (\w+)', str(a))
                    delTable.append(m[3])
                    namesTables.append(m[3])  # заполняем массив имен таблиц
                    # print(m[3])
                    columnsTables.append([a])  # заполняем имена таблиц в массиве колонок (чтобы потом удалить)
                else:
                    m = re.match('.\s*(\w+) (\w+): (\w+)', str(a))
                    namesTables.append(m[3])  # заполняем массив имен таблиц
                    # print(m[3])
                    columnsTables.append([a])  # заполняем имена таблиц в массиве колонок (чтобы потом удалить)
            else:
                if len(namesTables) == 0:
                    n = i
                    while '  Имя таблицы:' not in data_file[n]:
                        n -= 1
                    print(data_file[n])
                    m = re.match('.\s*(\w+) (\w+): (\w+)', str(data_file[n]))
                    print(m[3])
                    namesTables.append(m[3])
                    columnsTables.append(
                        [data_file[n]])  # заполняем имена таблиц в массиве колонок (чтобы потом удалить)
                    a = data_file[int(i)]
                columnsTables[-1].append(a)  # заполняем массив с полями таблиц
    print('del', delTable)
    for i, item in enumerate(columnsTables):
        del columnsTables[i][0]  # удаляем имена таблиц, чтобы были столбцы в чистом виде
    deps = []
    print(namesTables)
    for table in namesTables:
        y = [x['dep'] for x in tablesDep if x['table_name'] == table]  # получили номера департаментов,
        # пользователи которых должны получить уведомления
        deps.append(y)
    departIdUser = test_bd.getData(deps)

    print(namesTables)  # индексы названий таблиц соответствуют индексам депратаментов, индексам idUser и даннымв
    # списке columnsTables
    print(columnsTables)
    print(deps)
    print(departIdUser)
    #
    # print(namesTables)  # названия измененных таблиц
    # print(columnsTables)  # измененные колонки таблиц
    for index, name in enumerate(namesTables):
        flag = False
        userId = departIdUser[index][1]
        print(userId)
        if len(delTable) != 0 or len(namesTables) != 0:
            for i, it in enumerate(delTable):
                if delTable[i] == namesTables[index]:
                    sendMes(userId, 'Таблица ' + namesTables[index] + ' удалена')
                    flag = True
            if flag:
                continue
            else:
                for ind, i in enumerate(columnsTables[index]):
                    if '?' in i:  # фильтр по
                        # изменению
                        send_change.append(columnsTables[index][ind - 1])
                        send_change.append(columnsTables[index][ind - 2])

                        for ch in send_change:
                            if ch in send_add:
                                x = send_add.index(ch)
                                del send_add[x]
                            if ch in send_del:
                                y = send_del.index(ch)
                                del send_del[y]
                        break
                    elif '+' in i and '^' not in i:  # фильтр по добавлению
                        if i not in send_change:
                            send_add.append(i)
                        else:
                            break
                    elif '-' in i and '^' not in i:  # фильтр по удалению
                        if i not in send_change:
                            send_del.append(i)
                        else:
                            break
                if len(send_change) != 0:
                    send_change.insert(0, 'Произошло изменение в следующих полях: ')
                    send_change.insert(0, 'Таблица: ' + namesTables[index])
                    for item1 in send_change:
                        sendMes(userId, item1)
                if len(send_add) != 0:
                    send_add.insert(0, 'Произошло добавление следующих полей: ')
                    send_add.insert(0, 'Таблица: ' + namesTables[index])
                    for item1 in send_add:
                        sendMes(userId, item1)
                if len(send_del) != 0:
                    send_del.insert(0, 'Произошло удаление следующих полей: ')
                    send_del.insert(0, 'Таблица: ' + namesTables[index])
                    for item1 in send_del:
                        sendMes(userId, item1)
        send_add = []  # сюда отфильтровываются только данные по добавлению
        send_del = []  # сюда отфильтровываются только данные по удалению
        send_change = []  # сюда отфильтровываются только данные по изменению

    return namesTables


def call_repeatedly(interval, func, *args):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)

    threading.Thread(target=loop).start()
    return stopped.set


namesTablesDep = [{'table_name': 'Category', 'dep': ''}, {'table_name': 'Customer', 'dep': '2'},  # заменить
                  # департамент таблицы Customer на 3
                  {'table_name': 'Fabricator', 'dep': '4'}, {'table_name': 'Gender', 'dep': '3'},
                  {'table_name': 'Orders', 'dep': '3'}, {'table_name': 'Product', 'dep': '2'},
                  {'table_name': 'Size', 'dep': '4'}, {'table_name': 'Status', 'dep': '3'},
                  {'table_name': 'Supplier', 'dep': '4'}, {'table_name': 'test_table', 'dep': '3'},
                  {'table_name': 'tree_sample', 'dep': '2'}]
call_repeatedly(10, sendWarning, namesTablesDep)

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
