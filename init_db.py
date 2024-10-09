import sqlite3
connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()

cur.execute("INSERT INTO accounts (user_name, pass_word, email) VALUES (?,?,?)",
    ('admin_1', '123456', 'admin_1@gmail.com'))
cur.execute ("INSERT INTO accounts (user_name, pass_word, email) VALUES (?,?,?)",
    ('admin_2', '123456', 'admin_2gmail.com'))
connection.commit()
connection.close()