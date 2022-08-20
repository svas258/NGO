from multiprocessing import connection
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
     connection.executescript(f.read())
cur= connection.cursor()
cur.execute("INSERT INTO posts(NGO_NAME,contact_No,email) VALUES (?,?,?)",
            ('TEAMA','9901128055','svas258@gmail.com') )
connection.commit()
connection.close()
