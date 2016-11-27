'''

What should be done:

1. Aggregate by year UPD done

2. All internationals -- to dummy node (actually, scratch that: we can filter them post factum, because there are no internationals in lookup table!

3. Remove nonsense (maybe?..) UPD no, nonsense can stay

'''

import sqlite3
import networkx as nx

conn = sqlite3.connect('database/bfdatabase.db')

c = conn.cursor()

# like iterate over all files for a year (for all years, ofc)

years = [1993, 2015]
quarters = [1,2,3,4]

dir_path = 'graphs/'

for y in years:
	YG=nx.DiGraph() #a graph to hold all the data for a particular year
	for q in quarters:
		file_path=(str(y)+'_Q'+str(q)+'.gexf')
		full_path=(dir_path+file_path)
		QG=nx.read_gexf(full_path) # QG = "Quarter Graph"
		#now get it all in Year Graph (YG)
		for u,v,data in QG.edges_iter(data=True):
			if YG.has_node(u) is not True:
				YG.add_node(u, market_id=QG.node[u]['market_id'])
			if YG.has_node(v) is not True:
				YG.add_node(v, market_id=QG.node[v]['market_id'])
			if YG.has_edge(u,v):
				old = YG.get_edge_data(u,v)
				YG.add_edge(u,v,num_of_people=old['num_of_people'] + data['num_of_people'], total_price=old['total_price']+data['total_price'])
			else:
				YG.add_edge(u,v,num_of_people=data['num_of_people'], total_price=data['total_price'])
		
		#now add to the table


	for node,data in YG.nodes_iter(data=True):
		in_peop = YG.in_degree(node, weight='num_of_people')
		out_peop = YG.out_degree(node, weight='num_of_people')
		in_price = YG.in_degree(node, weight='total_price')
		out_price = YG.out_degree(node, weight='total_price')
		year = y
		market_id = data['market_id']
		unique_id = int(float(str(int(float(node))) + str(year))) #this is a mess
		row = (unique_id, node, market_id, in_peop, out_peop, in_price, out_price, year)
		c.execute('INSERT INTO airports VALUES (?,?,?,?,?,?,?,?)', row)

conn.commit()
conn.close()

