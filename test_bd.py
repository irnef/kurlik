from sqlalchemy import create_engine, MetaData, Table, text
from datetime import datetime
from sqlalchemy.connectors import pyodbc
import difflib
import numpy as np
from pathlib import Path

# import tbot

server = 'IRNEF\SQLEXPRESS'
database_testBD = 'test_bd'
database_BMS = 'BMS'


def makeEngine(server, database):
    engine = create_engine(
        'mssql+pyodbc://irnef:12345678@' + server + '/' + database + '?driver=ODBC+Driver+17+for+SQL+Server')
    return engine


def makeConnection(engine):
    try:
        conn = engine.connect()
        print("Connection done")
    except ConnectionError as e:
        print(f"The error '{e}' occurred")

    return conn


def makeMeta(engine):
    metadata = MetaData()
    metadata.reflect(engine)
    return metadata


def getScripts(engine):
    metadata_testBD = makeMeta(engine_testBD)
    tables_n = []  # имена таблиц
    tables = []  # объекты таблиц
    currentDate = datetime.now().date()
    currentTime = datetime.now().time()
    print(currentDate)
    fileName = str(currentDate) + 't' + str(currentTime.hour) + '-' + str(currentTime.minute) + '-' + str(
        currentTime.second) + ".txt"
    file = open(fileName, "w")
    keys = metadata_testBD.tables.keys()  # получение наименований таблиц
    for key in keys:
        tables_n.append(key)  # запись наименований таблиц в список
    # print(tables_n) # печать наименований всех таблиц
    # for i in metadata.tables:
    for n in range(len(tables_n)):
        name_t = tables_n[n]
        table = Table(name_t, metadata_testBD, autoload=True, autoload_with=engine)
        # print('Имя таблицы: ', tables_n[n])  # вывод информации о всех колонках каждой таблицы
        file.write('Имя таблицы: ' + tables_n[n] + '\n')
        for j in table.columns:
            #   print(j.name, j.type)
            file.write(str(j.name) + ', type: ' + str(j.type) + '\n')

    file.close()
    return file
    # print()


tableName = 'Users'
tableColumns = ' (surName, name, midName, isHead, departmentId, email, phoneNumber, pass, userIdBot) '
values1 = " ('Демидов', 'Артем', 'Андреевич', 1, 1, '123','123','123') "


def insData(tableName, tableColumns, values):
    # del values[4]
    values[3] = int(values[3])
    values[4] = int(values[4])
    engine_BMS = makeEngine(server, database_BMS)
    conn_BMS = makeConnection(engine_BMS)
    # metadata_BMS = makeMeta(engine_BMS)

    # getScripts(metadata_BMS, engine_BMS)

    # cursor = conn.cursor()
    # t = text("select * from Users")

    # t = text(
    #    "insert into " + tableName + " values ('" + str(values[0])+"','" + str(values[1]) +"','"+str(values[2])+"',"+\
    #   str(values[3]) + ',' + str(values[4]) + ',' + \
    #  "'"+str(values[5])+"','" + str(values[6])+"')")

    # t = text("insert into "+ tableName +" values ('"+ str(values[0]) +"',"+"'qwe', 'qwe', 1, 1, '123', '123', '123')")
    test = "insert into " + tableName + tableColumns + " values ('" + str(
        values[0]) + "', '" + str(values[1]) + "', '" + str(
        values[2]) + "', " + str(values[3]) + ", " + str(values[4]) + ", '" + str(values[5]) + "', '" + str(
        values[6]) + "','" + str(values[7]) + "','" + str(values[8]) + "')"

    t = text(test)
    result = conn_BMS.execute(t)
    # print(result.fetchall()) # отрабатывает при запуске select
    # conn.commit() # connection object has no attribute 'commit', но без него данные пишутся
    return result


# def compareFiles(file1, file2):  # выводит в 3 файл то, что в первом входном отличаетя от второго, удаленные элементы
#     # не выводит
#     with open(file1, 'r') as f1:
#         d = set(f1.readlines())
#
#     with open(file2, 'r') as f2:
#         e = set(f2.readlines())
#
#     open('file3.txt', 'a').close()
#     with open('file3.txt', 'a') as f:
#         for line in list(d - e):
#             f.write(line)


def compareDiff(file1, file2):
    diff = difflib.ndiff(open(file1).readlines(), open(file2).readlines())
    # print(*diff)
    # my_file = Path("C:/Users/user/Documents/file3.txt")
    file = open('file3.txt', 'w')
    for i in diff:
        file.write(i)
    # if my_file.exists():
    #     print('нашел')
    #     tbot.sendMes(392812944, 'привет')


engine_testBD = makeEngine(server, database_testBD)  # создание объекта бд, с которой нужно получать скрипты
conn_testBD = makeConnection(engine_testBD)

# c = metadata.tables[j]
# for i in c:
#     print(type)
# t = metadata.tables['Category']
# print(select([t]).compile())
# cursor = connection.cursor()
# cursor.execute("select * from test_bd.dbo.Orders")

# connection.commit()

# result = cursor.fetchall()
# result1 = cursor.fetchall()
# for i in result:
#   print(i)

conn_testBD.close()
