import operator
import networkx as nx
import csv

def nodes_connected(u, v):
	return u in G.neighbors(v)

with open('data/1020676917_T_DB1B_MARKET.csv', 'r') as data:
	G=nx.DiGraph()
	rows = csv.reader(data, quoting=csv.QUOTE_NONNUMERIC)
	next(rows) #skip the header
	for row in rows:
		row_fil = list(filter(lambda x: type(x) is float, row))
		if G.has_edge(row_fil[1], row_fil[2]):
			old = G.get_edge_data(row_fil[1], row_fil[2])
			G.add_edge(row_fil[1], row_fil[2], weight=old['weight'] + row_fil[3])
		else:
                        G.add_edge(row_fil[1], row_fil[2], weight=row_fil[3])
	
	wdict={}
	for v in G:
		wdict[v] = G.degree(v, weight='weight')
	swdict = sorted(wdict.items(), key=operator.itemgetter(1))

	print(swdict[-1])
	#nx.write_edgelist(G, 'edgelist.txt');
	#for a, b, data in sorted(G.edges(data=True), key=lambda abdata: abdata[2]['weight']):
	#	print('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))

