import sqlite3



con = sqlite3.connect("TeleBotDB.db")
cur = con.cursor()
cur.execute(f"""DELETE FROM Residents""")
con.commit()
con.close()