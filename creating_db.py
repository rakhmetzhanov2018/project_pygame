import sqlite3

con = sqlite3.connect('my.db')
cur = con.cursor()
cur.execute("""CREATE TABLE records (
   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   record INTEGER 
   );
""")
cur.execute("""INSERT INTO records (id, record) VALUES (1, 0)
""")

con.commit()
