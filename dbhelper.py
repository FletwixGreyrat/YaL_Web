from main import db, cursor
import datetime
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
               userId TEXT,
               userBot TEXT,
               firstname TEXT,
               surname TEXT,
               username TEXT,
               messages INTEGER,
               answers INTEGER,
               mygreet TEXT
)''')



cursor.execute("""CREATE TABLE IF NOT EXISTS allId(
               userBot TEXT,
               number INTEGER
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS activity(
               userBot TEXT,
               amountMessages INTEGER,
               amountAnswers INTEGER,
               date TEXT
)""")
# r = cursor.execute("SELECT * FROM users").fetchall()
# for i in r:
#     curdate = datetime.datetime.now().strftime("%d.%m,%Y")
#     cursor.execute(f"INSERT INTO activity (userBot, amountMessages, amountAnswers, date) VALUES ('{i[1]}', 0, 0, '{curdate}')")
db.commit()