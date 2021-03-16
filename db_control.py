import sqlite3
import json


def get_data(request):
    with sqlite3.connect("TelebotDB.db") as db:
        return db.execute(request)


def get_tracks_name():
    with sqlite3.connect("TeleBotDB.db") as db:
        return db.execute("SELECT name from Tracks").fetchall()

def add_new_row(username, chat_id):
    con = sqlite3.connect('TeleBotDB.db')
    cur = con.cursor()
    ids = [i[0] for i in cur.execute('''SELECT chatid FROM Residents''').fetchall()]
    print(ids)
    print(chat_id in ids)
    if chat_id not in ids:

        cur.execute(f'''
        INSERT INTO Residents (username, chatid) VALUES ("{username}", "{chat_id}")       
        ''')
    con.commit()
    con.close()



