from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.connectors import pyodbc

# import tbot

server = 'IRNEF\SQLEXPRESS'
# database = 'test_bd'
database = 'BMS'


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


def getScripts(metadata, engine):
    tables_n = []  # имена таблиц
    tables = []  # объекты таблиц
    keys = metadata.tables.keys()  # получение наименований таблиц
    for key in keys:
        tables_n.append(key)  # запись наименований таблиц в список
    # print(tables_n) # печать наименований всех таблиц
    for i in metadata.tables:
        for n in range(len(tables_n)):
            name_t = tables_n[n]
            table = Table(name_t, metadata, autoload=True, autoload_with=engine)
            # print('Имя таблицы: ', tables_n[n])  # вывод информации о всех колонках каждой таблицы
            # for j in table.columns:
            #     print(j.name, j.type)
            # print()


tableName = 'Users'
tableColumns = ' (surName, name, midName, isHead, departmentId, email, phoneNumber, pass) '
values = " ('Демидов', 'Артем', 'Андреевич', 1, 1, '123','123','123') "


def insData(tableName, tableColumns, values):
    # del values[4]
    values[3] = int(values[3])
    values[4] = int(values[4])
    engine = makeEngine(server, database)
    conn = makeConnection(engine)
    metadata = makeMeta(engine)
    getScripts(metadata, engine)

    # cursor = conn.cursor()
    # t = text("select * from Users")

    # t = text(
    #    "insert into " + tableName + " values ('" + str(values[0])+"','" + str(values[1]) +"','"+str(values[2])+"',"+\
    #   str(values[3]) + ',' + str(values[4]) + ',' + \
    #  "'"+str(values[5])+"','" + str(values[6])+"')")

    # t = text("insert into "+ tableName +" values ('"+ str(values[0]) +"',"+"'qwe', 'qwe', 1, 1, '123', '123', '123')")
    test = "insert into " + tableName + " values ('"+str(values[0])+"', '"+str(values[1])+"', '"+str(values[2])+"', "+str(values[3])+", "+str(values[4])+", '"+str(values[5])+"', '"+str(values[6])+"','"+str(values[7])+"')"
    t = text(test)
    result = conn.execute(t)
    # print(result.fetchall()) # отрабатывает при запуске select
    # conn.commit() # connection object has no attribute 'commit', но без него данные пишутся
    return result


engine = makeEngine(server, database)
conn = makeConnection(engine)
metadata = makeMeta(engine)
getScripts(metadata, engine)
# while 1:
#     if tbot.done:
#         print('попал') # не попадает
#         insData(tableName, tableColumns, tbot.dataReg)

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

conn.close()
