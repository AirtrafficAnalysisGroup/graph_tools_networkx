import sqlite3
import sys

database_path='database/'

if len(sys.argv) == 2:
	database_path += sys.argv[1]
else:
	database_path += 'bfdatabase.db'

conn = sqlite3.connect(database_path)

c = conn.cursor()

#for row in c.execute('SELECT * FROM airports'):
#	print(row)

for year in [1993,1994,1995,2050,2015]:
	c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND airport_id=?', (year,12892.0))
	print(c.fetchone())

conn.close()
