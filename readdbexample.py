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

all_ids = []

for m_id in c.execute('SELECT fl_id FROM lookup'):
	all_ids.append(m_id[0]) 

# for all markets

for m_id in all_ids:
	traffic = {}
	traffic_legacy = []
	employ = []
	for year in range(1994,2015):
		total_in = 0
		total_out = 0
		for q in range(1,4):
			rows_fl = c.execute('SELECT in_degree_people, out_degree_people FROM airports WHERE year=? AND market_id=? AND quarter=?', (year,m_id, q))
			for pair in rows_fl:
				total_in += pair[0]
				total_out += pair[1]
			rows_ec = c.execute('SELECT mean_value FROM econ_data WHERE year=? AND MSA_id_airline=? AND quarter=?', (year, int(m_id), q))
			#sum for all quarters
			total_ec = 0
			for value in rows_ec:
				total_ec += value[0]
			employ.append(total_ec/4)
		traffic[total_in+total_out] = year 
		traffic_legacy.append(total_in+total_out)
	pr_tr = 1000000000 #previous traffic (i.e. in previous quarter)
	prpr_tr = pr_tr
	for q_tr in traffic_legacy:
		if (float(q_tr)/float(pr_tr)) < 0.95 and (float(pr_tr)/float(prpr_tr)) < 0.95 and sum(traffic_legacy) > 5000000.0:
			names = c.execute('SELECT fl_name, fl_state FROM lookup WHERE fl_id=?', (m_id,))
			mar_name = ""
			for n in names:
				mar_name = (n[0] + ", " + n[1])
			print("There was a depression in ", mar_name, "in", traffic[q_tr])
		if q_tr == 0:
			continue
		prpr_tr = pr_tr
		pr_tr = q_tr


conn.close()
