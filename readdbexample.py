import sqlite3
import sys
import scipy
import numpy as np
import scipy.stats

database_path='database/'

if len(sys.argv) == 2:
	database_path += sys.argv[1]
else:
	database_path += 'bfdatabase.db'

# recovery from great recession?

# so for like all the markets (i.e. all market ids)
# get the sum(in_ and out_degree people), sum(in_ and out_ fares)
# if it drops more than a certain percent -- say there is decline there 

conn = sqlite3.connect(database_path)

c = conn.cursor()

#for row in c.execute('SELECT year FROM econ_data'):
#	print(row)

#print(list(map(lambda x: x[0], c.description)))

c.execute('SELECT fl_id FROM lookup WHERE fl_name=?', ('New York City',))

air_id = (c.fetchone())[0]


# for all markets

for year in range(1994,2016):
	for q in range(1,5):
		total_out = 0
		total_in = 0
		rows_fl = c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND market_id=? AND quarter=?', (year,air_id, q))
		for pair in rows_fl:
			total_in += pair[0]
			total_out += pair[1]
		rows_ec = c.execute('SELECT mean_value FROM econ_data WHERE year=? AND MSA_id_airline=? AND quarter=?', (year, int(air_id), q))
		total_ec = 0
		for value in rows_ec:
			total_ec += value[0]
		out = str(year)+"Q"+str(q)+","+str(total_in+total_out)+","+str(total_ec/4)
		print(out)

conn.close()
