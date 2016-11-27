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

c.execute('SELECT * FROM lookup')

#print(list(map(lambda x: x[0], c.description)))

c.execute('SELECT fl_id FROM lookup WHERE fl_name=?', ('New York City',))

air_id = (c.fetchone())[0]

print(air_id)

for year in range(1993,2015):
	rows = c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND market_id=?', (year,air_id))
	print(year)
	#now sum for all airports
	total_in = 0
	total_out = 0
	for pair in rows:
		total_in += pair[0]
		total_out += pair[1]
	print(total_in, total_out)

conn.close()
