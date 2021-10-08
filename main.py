import sqlite3 as sql
from typing import Tuple
import pandas as pd
import guiwindow
import sys


def open_db(filename: str) -> Tuple[sql.Connection, sql.Cursor]:
    db_connection = sql.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sql.Connection):
    connection.close()


def setup_employees(cursor: sql.Cursor, conn: sql.Connection):
    cursor.execute("""DROP TABLE IF EXISTS employees""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees(employeeID INTEGER PRIMARY KEY,
                        fname TEXT NOT NULL,
                        lname TEXT NOT NULL,
                        title TEXT NOT NULL,
                        active INTEGER DEFAULT 0,
                        reorder INTEGER DEFAULT 0);""")
    conn.commit()


def get_data():
    employees = pd.read_csv('taco_employees.csv')
    return employees


def populate_employees(cursor: sql.Cursor, conn: sql.Connection):
    employees = get_data()
    keys = employees['Employee ID'].tolist()
    data_dict = {}
    for item in keys:
        data_dict[item] = (employees.loc[employees['Employee ID'] == item]['First Name'].tolist()[0],
                           employees.loc[employees['Employee ID'] == item]['Last Name'].tolist()[0],
                           employees.loc[employees['Employee ID'] == item]['Title'].tolist()[0],
                           employees.loc[employees['Employee ID'] == item]['Active'].tolist()[0],
                           employees.loc[employees['Employee ID'] == item]['Can Reorder?'].tolist()[0])

    for key in data_dict.keys():
        cursor.execute("""INSERT INTO employees (employeeID, fname, lname, title, active, reorder)
                        VALUES (?,?,?,?,?,?)""", (key, data_dict[key][0], data_dict[key][1],
                                                  data_dict[key][2], data_dict[key][3], data_dict[key][4]))
    conn.commit()


# This is for testing. Show them this
def select_from(curs: sql.Cursor):
    curs.execute("""SELECT * FROM employees""")
    data = curs.fetchall()
    #print(data)


def main():
    # Main database stuff here
    name = 'taco_tower.db'
    conn, curs = open_db(name)
    setup_employees(curs, conn)
    populate_employees(curs, conn)
    select_from(curs)
    # get_info(cursor, id) # May want to consider including this in GUI
    app = guiwindow.QApplication(sys.argv)
    ex = guiwindow.Window(conn, curs)
    ex.isHidden()
    sys.exit(app.exec_())

main()