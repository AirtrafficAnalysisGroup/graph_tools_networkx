import sqlite3
import sys

database_path='database/'

if len(sys.argv) == 2:
	database_path += sys.argv[1]
else:
	database_path += 'bfdatabase.db'

conn = sqlite3.connect(database_path)

c = conn.cursor()

for row in c.execute('SELECT * FROM airports'):
	print(row)

#c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND airport_id=?', (1993,12892.0))

#print(c.fetchone())

conn.close()
