import difflib
import sqlite3 as sq
from datetime import datetime

import sqlalchemy as sa


def makeEngine(bd):
    try:
        engine = sa.create_engine('sqlite:///' + bd)
        print('Engine OK')
    except:
        print('Engine Error')
    return engine


def makeConnection(bd):
    try:
        conn = sq.connect(bd)
        print("Connection done")
        return conn
    except ConnectionError as e:
        print("Error connection")
        # print("The error '{e}' occurred")


def createCurs(conn):
    crs = conn.cursor()
    #  crs.execute('''select * from Users''')  # Строка для теста
    #  print(crs.fetchall())
    conn.commit()
    return crs


def makeMeta(engine):
    meta = sa.MetaData()
    meta.reflect(engine)
    print(meta.tables)
    for i in meta.tables:
        print(i)
    print(dict.values(meta.tables))
    tables_n = []  # имена таблиц
    tables = []  # объекты таблиц
    keys = meta.tables.keys()  # получение наименований таблиц
    tables_n = [key for key in keys]  # запись наименований таблиц в список
    fileName = datetime.strftime(datetime.now(), '%Y-%m-%dt%H-%M-%S.txt')
    file = open(fileName, "w")
    print(fileName)
    print(tables_n)
    for n in range(len(tables_n)):
        name_t = tables_n[n]
        table = sa.Table(name_t, meta, autoload=True, autoload_with=engine)
        print('TableName: ', tables_n[n])  # вывод информации о всех колонках каждой таблицы
        file.write('TableName: ' + tables_n[n] + '\n')
        for j in table.columns:
            print(j.name, j.type)
            file.write(str(j.name) + ', type: ' + str(j.type) + '\n')

    file.close()
    return file


# def getScripts(engine):
#     metadata_testBD = makeMeta(engine_testBD)
#     tables_n = []  # имена таблиц
#     tables = []  # объекты таблиц
#     fileName = datetime.strftime(datetime.now(), '%Y-%m-%dt%H-%M-%S.txt')
#     print(fileName)
#     file = open(fileName, "w")
#     keys = metadata_testBD.tables.keys()  # получение наименований таблиц
#     tables_n = [key for key in keys]  # запись наименований таблиц в список
#     # print(tables_n) # печать наименований всех таблиц
#     # for i in metadata.tables:
#     for n in range(len(tables_n)):
#         name_t = tables_n[n]
#         table = Table(name_t, metadata_testBD, autoload=True, autoload_with=engine)
#         # print('Имя таблицы: ', tables_n[n])  # вывод информации о всех колонках каждой таблицы
#         file.write('Имя таблицы: ' + tables_n[n] + '\n')
#         for j in table.columns:
#             #   print(j.name, j.type)
#             file.write(str(j.name) + ', type: ' + str(j.type) + '\n')
#
#     file.close()
#     return file
#     # print()

tableName = 'Users'
tableColumns = ' (surName, name, midName, isHead, departmentId, email, phoneNumber, pass, userIdBot) '
values1 = " ('Демидов', 'Артем', 'Андреевич', 1, 1, '123','123','123') "


# def insData(tableName, tableColumns, values):
#     # del values[4]
#     values[3] = int(values[3])
#     values[4] = int(values[4])
#     engine_BMS = makeEngine(server, database_BMS)
#     conn_BMS = makeConnection(engine_BMS)
#     # metadata_BMS = makeMeta(engine_BMS)
#
#     # getScripts(metadata_BMS, engine_BMS)
#
#     # cursor = conn.cursor()
#     # t = text("select * from Users")
#     try:
#         test = "insert into " + tableName + tableColumns + " values ('" + str(
#             values[0]) + "', '" + str(values[1]) + "', '" + str(
#             values[2]) + "', " + str(values[3]) + ", " + str(values[4]) + ", '" + str(values[5]) + "', '" + str(
#             values[6]) + "','" + str(values[7]) + "','" + str(values[8]) + "')"
#
#         t = text(test)
#         result = conn_BMS.execute(t)
#         return result
#     except Exception:
#         print('Ошибка ввода данных')
#         return 'Error'
#     # print(result.fetchall()) # отрабатывает при запуске select
#     # conn.commit() # connection object has no attribute 'commit', но без него данные пишутся


def getData(depsid):
    print(depsid)
    departIdUser = []
    connSysBd = makeConnection(sysBD)
    crs = connSysBd.cursor()
    for i, dep in enumerate(depsid):
        dep_s = ''.join(depsid[i])
        print(dep_s)
        # t = sa.text("select departmentId, userIdBot from Users where departmentId = " + dep_s)
        t = '''select departmentId, userIdBot from Users where departmentId = '''
        crs.execute('''select departmentId, userIdBot from Users where departmentId = 1''')
        result = []
        #  crs.execute('''select * from Users''')  # Строка для теста
        print(crs.fetchall())
        for j in result:
            departIdUser.append(j)
    connSysBd.commit()
    connSysBd.close()
    return departIdUser


# def checkPas():


def compareDiff(file1, file2):
    diff = difflib.ndiff(open(file1).readlines(), open(file2).readlines())
    file = open('file3.txt', 'w')
    file1 = open('test.txt', 'w')
    for i in diff:
        file.write(i)
        file1.write(i)


sysBD = 'prob_bd.db'  # Системная БД
clientBD = 'test_bd_lite.db'  # Клиентская БД (обрабатываемая БД)
#  conn_testBD = makeConnection('prob_bd.db')
#  createCurs(conn_testBD)
engineSysBd = makeEngine('prob_bd.db')

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
