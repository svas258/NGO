from multiprocessing import connection
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
     connection.executescript(f.read())
cur= connection.cursor()
cur.execute("INSERT INTO posts(NGO_NAME,contact_No) VALUES (?,?)",
            ('TEAMA','9901128055') )
connection.commit()
connection.close()
