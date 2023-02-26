import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO stocks (title, price) VALUES (?, ?)", ('First post', 'Ksh 3000'))
cursor.execute("INSERT INTO stocks (title, price) VALUES (?, ?)", ('Second post', 'Ksh 3500'))


connection.commit()


connection.close()