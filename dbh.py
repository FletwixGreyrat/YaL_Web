import sqlite3

db1 = sqlite3.connect('data1.db')
cursor1 = db1.cursor()

db2 = sqlite3.connect('data.db')
cursor2 = db2.cursor()


lst1 = cursor2.execute('SELECT * FROM users').fetchall()
lst2 = cursor2.execute('SELECT * FROM allId').fetchall()
lst3 = cursor2.execute('SELECT * FROM activity').fetchall()

cursor1.execute('''CREATE TABLE IF NOT EXISTS users(
                userId TEXT,
                userBot TEXT,
                messages INTEGER,
                answers INTEGER,
                mygreet TEXT,
                number INTEGER,
                amountMessages INTEGER,
                amountAnswers INTEGER,
                date TEXT
)''')
db1.commit()

for i in range(155):
    cursor1.execute(f'''INSERT INTO users (userId, userBot, messages, answers, mygreet, number, amountMessages, amountAnswers, date) VALUES ("{lst1[i][0]}", "{lst1[i][1]}", {lst1[i][5]}, {lst1[i][6]}, "{lst1[i][7]}", {lst2[i][1]}, {lst3[i][1]}, {lst3[i][2]}, "{lst3[i][3]}")''')

db1.commit()