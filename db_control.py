import sqlite3
import json


def get_data(request):
    with sqlite3.connect("TelebotDB.db") as db:
        return db.execute(request)

def get_proffessions():
    with sqlite3.connect("TeleBotDB.db") as db:
        return db.execute("SELECT name From skills").fetchall()

def get_tracks_name():
    with sqlite3.connect("TeleBotDB.db") as db:
        return db.execute("SELECT name from Tracks").fetchall()



def add_new_member(contact):
    pass


def get_all_id_for_group(group):
    with sqlite3.connect("TeleBotDB.db") as db:
        return db.execute(f"""SELECT chatid FROM Residents WHERE track = (SELECT id FROM tracks WHERE name = '{group}')""").fetchall()

