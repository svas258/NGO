from multiprocessing import connection
import sqlite3
password='9901128055'
tak=[('ram','9901128066','user'),('srini','9901128055','admin' )]
connection = sqlite3.connect('database.db')
#with open('user.sql') as f:
#     connection.executescript(f.read())
cur= connection.cursor()
cur.executemany("INSERT INTO users(user,password,role) VALUES (?,?,?)",tak)
u=cur.execute("SELECT id FROM users ").fetchall()
#p=cur.execute("SELECT * FROM users where password=?",(password,)).fetchone()
print(u)

connection.commit()
connection.close()
