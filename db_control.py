import sqlite3
import json





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
