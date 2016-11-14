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
		if G.has_edge(row_fil[0], row_fil[1]):
			old = G.get_edge_data(row_fil[0], row_fil[1])
			G.add_edge(row_fil[0], row_fil[1], num_of_people=old['num_of_people'] + row_fil[2], total_price=old['total_price'] + row_fil[3])
		else:
			G.add_edge(row_fil[0], row_fil[1], num_of_people=row_fil[2], total_price=row_fil[3])

	output_file_path = ('graphs/' + name + '.edgelist') 
	nx.write_edgelist(G, output_file_path);

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
