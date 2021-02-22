import sqlite3
import json



con = sqlite3.connect('TeleBotDB.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS "Residents" (
        "id"	INTEGER INCREMENT DEFAULT 0,
        "Name"	TEXT NOT NULL,
        "Number"	TEXT NOT NULL,
        "Profession"	TEXT NOT NULL,
        "Rank"	INTEGER NOT NULL DEFAULT 0,
        "Track"	TEXT NOT NULL,
        "Education"	TEXT NOT NULL,
        "Old"	INTEGER NOT NULL,
        "Group_id" INTEGER NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "Groups" (
        "Name"  TEXT UNIQUE NOT NULL,
        "GroupId" INTEGER INCREMENT)''')


create_tables()


