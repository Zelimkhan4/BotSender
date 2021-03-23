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


def get_all_groups():
    with sqlite3.connect("TeleBotDB.db") as db:
        return db.execute(f"""SELECT name FROM Groups""").fetchall()


def get_all_residents():
    with sqlite3.connect("TeleBotDB.db") as db:
        return db.execute(f"""SELECT name, surname FROM Residents""").fetchall()

def add_new_group(name, participants):
    with sqlite3.connect("TeleBotDB.db") as db:
        db.execute(f"""INSERT INTO Groups (name) VALUES {name}""").fetchall()
        db.commit()
        for name, surname in participants:
            groups = db.execute(f"SELECT groups from Residents WHERE name = {name} and surname = {surname}")
            groups = tuple(list(new_group).append(db.execute(f"SELECT id from Groups WHERE name = '{name}'")[0]))
            db.execute(f"UPDATE Residents SET groups = '{groups}' WHERE name = '{name}' and surname = '{surname}'")
            db.commit()
            print(67)