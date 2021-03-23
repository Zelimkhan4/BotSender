import sqlite3


db = sqlite3.connect('TeleBotDB.db')
db.execute('DELETE from Residents')
db.commit()