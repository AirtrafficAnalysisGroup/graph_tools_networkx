'''

What should be done:

1. Aggregate by year UPD done

2. All internationals -- to dummy node (actually, scratch that: we can filter them post factum, because there are no internationals in lookup table!

3. Remove nonsense (maybe?..) UPD no, nonsense can stay

'''

import sqlite3
import networkx as nx
import sys

database_path='database/'

if len(sys.argv) == 2:
	database_path += sys.argv[1]
else:
	database_path += 'bfdatabase.db'

conn = sqlite3.connect(database_path)

c = conn.cursor()

# like iterate over all files for a year (for all years, ofc)

#years = [2050]
years = [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
quarters = [1,2,3,4]

dir_path = 'graphs/'

for y in years:
	for q in quarters:
		file_path=(str(y)+'_Q'+str(q)+'.gexf')
		full_path=(dir_path+file_path)
		QG=nx.read_gexf(full_path) # QG = "Quarter Graph"

		for node,data in QG.nodes_iter(data=True):
			in_peop = QG.in_degree(node, weight='num_of_people')
			out_peop = QG.out_degree(node, weight='num_of_people')
			in_price = QG.in_degree(node, weight='total_price')
			out_price = QG.out_degree(node, weight='total_price')
			market_id = data['market_id']
			unique_id = int(float(str(int(float(node))) + str(y) + str(q))) #this is a mess
			row = (unique_id, node, market_id, in_peop, out_peop, in_price, out_price, y, q)
			c.execute('INSERT INTO airports VALUES (?,?,?,?,?,?,?,?,?)', row)
	print("Done for ", y)

conn.commit()
conn.close()

