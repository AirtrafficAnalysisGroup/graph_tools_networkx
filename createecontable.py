import sqlite3
import csv

econ_table_path = 'data/all_grouped_MSA_year_quarter_with_lookup_csv.csv'

database_path='database/bfdatabase.db'

conn = sqlite3.connect(database_path)

c = conn.cursor()

#id INTEGER PRIMARY KEY NOT NULL, MSA_id_economy [0] INTEGER NOT NULL, year [1] INTEGER NOT NULL, quarter [2] INTEGER NOT NULL, mean_value [3]  REAL NOT NULL, MSA_id_airline [4] INTEGER NOT NULL

c.execute('CREATE TABLE econ_data (id INTEGER PRIMARY KEY NOT NULL, MSA_id_economy INTEGER NOT NULL, year INTEGER NOT NULL, quarter INTEGER NOT NULL, mean_value REAL NOT NULL, MSA_id_airline INTEGER NOT NULL);')

with open(econ_table_path, 'r') as econ_t:
	er = csv.reader(econ_t) #er = econ reader
	next(er) #skip the header
	for row in er:
		unique_id = int(float(row[0]+row[1]+row[2]))
		to_db=(unique_id, int(float(row[0])), int(float(row[1])), int(float(row[2])), float(row[3]), int(row[4]))
		c.execute('INSERT INTO econ_data VALUES(?,?,?,?,?,?)', to_db)

conn.commit()
conn.close()
