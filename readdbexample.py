import sqlite3

conn = sqlite3.connect('database/bfdatabase.db')

c = conn.cursor()

c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND airport_id=?', (1993,12892.0))

print(c.fetchone())

conn.close()
