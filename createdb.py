#creates database, with empty airport table and a lookup table

import sqlite3
import csv

conn = sqlite3.connect('database/bfdatabase.db')

c = conn.cursor()

c.execute('CREATE TABLE airports (id REAL PRIMARY KEY NOT NULL, market_id REAL NOT NULL, in_degree_people REAL, out_degree_people REAL, in_degree_fare REAL, out_degree_fare REAL, year INT);')

conn.commit()

# now the lookup table

c.execute('CREATE TABLE lookup (id INT PRIMARY KEY NOT NULL, ec_name TEXT NOT NULL, ec_state TEXT NOT NULL, ec_id REAL NOT NULL, fl_name TEXT NOT NULL, fl_state TEXT NOT NULL, fl_id REAL NOT NULL);')

with open('lookup/merged_lookup.csv', 'r') as lookup:
	id = 0
	lr = csv.reader(lookup) #lr stands for 'lookup reader', duh
	for row in lr:
		id += 1
		to_db = (id, row[0], row[1], row[2], row[3], row[4], row[5])
		c.execute('INSERT INTO lookup VALUES (?,?,?,?,?,?,?)', to_db)

#check that all is fine

for row in c.execute('SELECT * FROM lookup WHERE ec_state=?', ('NC',)):
	print(row)

conn.commit()

conn.close()
