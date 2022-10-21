import sqlite3
connection_obj = sqlite3.connect('database.db')
cursor_obj = connection_obj.cursor()
cursor_obj.execute("DROP TABLE IF EXISTS Users")
table =""" CREATE TABLE Users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      public_id INTEGER ,
      name TEXT NOT NULL,
      password VARCHAR NOT NULL,
      admin BOOLEAN NOT NULL
);"""
cursor_obj.execute(table)
print("Table is Ready")
connection_obj.close()
