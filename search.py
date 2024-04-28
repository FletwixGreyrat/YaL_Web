import sqlite3

data = sqlite3.connect('data.db')

cursor = data.cursor()

d = cursor.execute('SELECT * FROM users WHERE userBot="140598113387760"').fetchone()