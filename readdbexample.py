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
# introduce a lag: econ data should lag flight data by say a year
# get the sum(in_ and out_degree people), sum(in_ and out_ fares)
# run Pearson

conn = sqlite3.connect(database_path)

c = conn.cursor()

#for row in c.execute('SELECT year FROM econ_data'):
#	print(row)

#print(list(map(lambda x: x[0], c.description)))

all_ids = []

for m_id in c.execute('SELECT fl_id FROM lookup'):
	all_ids.append(m_id[0]) 

# for all markets

for m_id in all_ids:
	traffic = []
	employ = []
	for year in range(1994,2015):
		for q in range(1,4):
			rows_fl = c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND market_id=? AND quarter=?', ((year-1),m_id, q))
			#now sum for all airports
			total_in = 0
			total_out = 0
			for pair in rows_fl:
				total_in += pair[0]
				total_out += pair[1]
			rows_ec = c.execute('SELECT mean_value FROM econ_data WHERE year=? AND MSA_id_airline=? AND quarter=?', (year, int(m_id), q))
			#sum for all quarters
			total_ec = 0
			for value in rows_ec:
				total_ec += value[0]
			traffic.append(total_in+total_out)
			employ.append(total_ec/4)
	coeff, p_val = scipy.stats.pearsonr(traffic, employ)
	if p_val < 0.05 and sum(traffic) > 5000000.0:
		names = c.execute('SELECT fl_name, fl_state FROM lookup WHERE fl_id=?', (m_id,))
		mar_name = ""
		for n in names:
			mar_name = (n[0] + ", " + n[1])
		print(mar_name, "Coeff: ", coeff, "p_val: ", p_val)


conn.close()
