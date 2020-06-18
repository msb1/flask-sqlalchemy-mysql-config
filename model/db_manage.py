import sqlite3
import mysql.connector
import pandas as pd

'''
Test routine for generating database test data
'''

app_tables = ['equip', 'continuous', 'discrete', 'alert']

equip = [
    [1, 'scanner', 'eline', '034', 'fab', True, 0.08, 0.6, 'scan01-34'],
    [2, 'printer', 'eline', '034', 'fab', True, 0.07, 0.55, 'print02-34'],
    [3, 'hacker', 'uline', '037', 'fab', False, 0.1, 0.45, 'hack03-37'],
    [4, 'cvd', 'wline', '045', 'fab', False, 0.04, 0.4, 'hack03-37'],
    [5, 'clean', 'eline', '034', 'fab', False, 0.11, 0.65, 'hack03-37'],
]

continuous = [
    [1, 'sens1', 1, 0, 100, 'uni', 10, 80, 70, 100],
    [2, 'sens2', 1, 10, 200, 'norm', 40, 20, 80, 20],
    [3, 'sens3', 1, 0, 250, 'log', 5, 10, 10, 10],
    [4, 'sens4', 1, 0, 400, 'uni', 250, 400, 10, 300],
    [5, 'sens5', 1, 50, 350, 'uni', 50, 300, 200, 350],
    [6, 'sens6', 1, 0, 250, 'norm', 50, 20, 100, 40],
    [7, 'sens7', 1, 50, 500, 'norm', 200, 40, 400, 50],
    [8, 'sens8', 1, 100, 350, 'uni', 200, 350, 100, 250],
    [9, 'sens9', 1, 0, 50, 'log', 1, 4, 10, 5]
]

discrete = [
    [1, 'disc01', 1, 2, 'fail, pass', '0.1, 0.9', '0.9, 0.1'],
    [2, 'disc02', 1, 3, 'negative, neutral, positive', '0.2,0.4,0.4', '0.8, 0.2, 0.0'],
    [3, 'disc03', 1, 3, 'off, hold, run', '0.2,0.2,0.6', '0.6, 0.4, 0.0'],
    [4, 'disc04', 1, 2, 'good, bad', '0.7, 0.3', '0.3, 0.7'],
    [5, 'disc05', 1, 5, 'veryneg, neg, neut, pos, verypos', '0.0, 0.1, 0.3, 0.3, 0.3', '0.6, 0.2, 0.2, 0.0, 0.0'],
    [6, 'disc06', 1, 2, 'negative, neutral, positive', '0.3, 0.3, 0.4', '0.5, 0.3, 0.2'],
]

alert = [
    [1, 'alert1', 1, 'alert', 45, 80, True],
    [2, 'warn2', 2, 'warn', 340, 780, False],
    [3, 'alarm3', 1, 'alarm', 50, 90, False],
    [4, 'warn4', 1, 'warn', 34, 100, False],
]


def main():
    # con = sqlite3.connect('config.db')
    con = mysql.connector.connect(
        host='192.168.248.4',
        port='3306',
        user='barnwaldo',
        password='shakeydog',
        database='equipconfig'
    )

    cursor = con.cursor()

    cursor.execute("DROP TABLE IF EXISTS equip")
    # for sqlite change VARCHAR to TEXT 

    cursor.execute(
        "CREATE TABLE equip(eid INTEGER PRIMARY KEY NOT NULL UNIQUE, name VARCHAR(100), line VARCHAR(100), lineid VARCHAR(50),"
        + "etype VARCHAR(100), simulator BOOLEAN, errate FLOAT, success FLOAT, filename VARCHAR(50))")

    for e in equip:
        cursor.execute("INSERT INTO equip VALUES({}, '{}', '{}', '{}', '{}', {}, {}, {}, '{}')".format(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8]))
    con.commit()

    cursor.execute("DROP TABLE IF EXISTS continuous")
    cursor.execute("CREATE TABLE continuous(cid INTEGER PRIMARY KEY NOT NULL UNIQUE, name VARCHAR(100), eid INTEGER, cmax FLOAT, cmin FLOAT ," 
                   + "distribution VARCHAR(50), posparam1 FLOAT, posparam2 FLOAT, negparam1 FLOAT, negparam2 FLOAT)")

    for c in continuous:
        cursor.execute("INSERT INTO continuous VALUES({}, '{}', '{}', {}, {}, '{}', {}, {}, {}, {})".format(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]))
    con.commit()

    cursor.execute("DROP TABLE IF EXISTS discrete")
    cursor.execute(
        "CREATE TABLE discrete(dd INTEGER PRIMARY KEY NOT NULL UNIQUE, name VARCHAR(100), eid INTEGER, numlevels INTEGER, levels VARCHAR(500),"
        + "posprobs VARCHAR(500), negprobs VARCHAR(500))")

    for d in discrete:
        cursor.execute("INSERT INTO discrete VALUES({}, '{}', '{}', {}, '{}', '{}', '{}')".format(d[0], d[1], d[2], d[3], d[4], d[5], d[6]))
    con.commit()

    cursor.execute("DROP TABLE IF EXISTS alert")
    cursor.execute("CREATE TABLE alert(aid INTEGER PRIMARY KEY NOT NULL UNIQUE, name VARCHAR(100), eid INTEGER, atype text,"
                   + "warnlevel FLOAT, alarmlevel FLOAT, increasing BOOLEAN)")

    for a in alert:
        cursor.execute("INSERT INTO alert VALUES({}, '{}', '{}', '{}', {}, {}, {})".format(
            a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
    con.commit()

    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")          # sqlite
    cursor.execute("SELECT table_name FROM information_schema.tables;")             # MySQL
    tables = cursor.fetchall()
    print(tables)
    for table_name in tables[-4:]:
        # print(table_name)
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, con)
        print("\n\n*****", table_name, "*****")
        print(table.head())
    cursor.close()
    con.close()


if __name__ == "__main__":
    main()
