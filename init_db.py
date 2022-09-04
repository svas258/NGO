from multiprocessing import connection
import sqlite3

connection = sqlite3.connect('database.db')
cur= connection.cursor()
cur.execute("SELECT * FROM users ")
a=cur.fetchone()
print(a)
connection.close()
