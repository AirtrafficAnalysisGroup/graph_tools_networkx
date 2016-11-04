'''

Created by Ruslan

Reads graphs from folders "data/[year]/[quarter]", builds graphs and saves them in edgelist format

'''
import operator
import networkx as nx
import csv
import os
import sys

def nodes_connected(u, v):
	return u in G.neighbors(v)

def build_graph_for_file(file_path, dir_name, name):
	data = open(file_path, 'r')
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
	output_file_path = ('graphs/' +dir_name +'/' + name + '.edgelist') 
	nx.write_edgelist(G, output_file_path);
	for a, b, data in sorted(G.edges(data=True), key=lambda abdata: abdata[2]['weight']):
	       print('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))

def main():
	if len(sys.argv) != 2:
		print("Correct use: python3 run.py [subfolder with graphs]")
		sys.exit()
	path = "data/" + sys.argv[1]
	testfiles = os.listdir(path)
	for file_path in testfiles:
		file_name = ((file_path).split('.'))[0]
		full_file_path = (path + '/' + file_path)
		build_graph_for_file(full_file_path, sys.argv[1], file_name)

if __name__ == "__main__":
	main()
