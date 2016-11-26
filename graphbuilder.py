'''

Created by Ruslan

Reads graphs from folders "data/[year]/[quarter]", builds graphs and saves them in edgelist format

Graph data format: "ORIGIN_AIRPORT_ID" [0],"ORIGIN_CITY_MARKET_ID" [1],"DEST_AIRPORT_ID" [2],"DEST_CITY_MARKET_ID" [3],"PASSENGERS" [4],"MARKET_FARE" [5]

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
		if G.has_node(row_fil[0]) is not True:
			G.add_node(row_fil[0], market_id=row_fil[1])
		if G.has_node(row_fil[2]) is not True:
			G.add_node(row_fil[2], market_id=row_fil[3])
		if G.has_edge(row_fil[0], row_fil[2]):
			old = G.get_edge_data(row_fil[0], row_fil[2])
			G.add_edge(row_fil[0], row_fil[2], num_of_people=old['num_of_people'] + row_fil[4], total_price=old['total_price'] + row_fil[5])
		else:
			G.add_edge(row_fil[0], row_fil[2], num_of_people=row_fil[4], total_price=row_fil[5])

	output_file_path = ('graphs/' + name + '.gexf') 
	nx.write_gexf(G, output_file_path)

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
