'''

Created by Ruslan

Creates a timeline: [name] [num of passengers at 1st point in time] [num of passengers at 2nd point in time]

'''


import os
import sys
import networkx as nx
import csv
from collections import defaultdict

class TimelineBuilder:
	''' Builds timelines and shit '''
	def __init__(self, lookup_path, dir_path):
		self.lookup_dict = prefill_dict_from_lookup(lookup_path)
		self.dir_path = dir_path
		self.timeline = defaultdict(list)  # using dictionary of lists to store {["Name of the city"], [list of the values]} 
	
	def build(self):
		years = [2050, 2051]
		quarters = [1]
		for y in years:
			for q in quarters:
				exist = {} #if for particular city there is no entry for this year, replace it with N/A
				for key in self.lookup_dict:
					exist[key] = 0
				path = self.dir_path + str(y) + "_Q" + str(q) + ".edgelist"
				fh = open(path, 'rb')
				G=nx.read_edgelist(fh, create_using=nx.DiGraph())
				fh.close()
				self.timeline["Name of the city"].append(("|" + str(y) + "_Q" + str(q) + " num of people" + "|" ))
				self.timeline["Name of the city"].append(("|" + str(y) + "_Q" + str(q) + " total price" + "|"))
				for n in G.nodes():
					total_weight = 0
					total_price = 0
					for neigh in G.neighbors(n):
						data = G.get_edge_data(n, neigh)
						total_weight += data['num_of_people']
						total_price += data['total_price']
					self.timeline[self.lookup_dict[n]].append(total_weight)
					self.timeline[self.lookup_dict[n]].append(total_price)
					exist[n] = 1
				for key, value in exist.items():
					if value == 0:
						self.timeline[self.lookup_dict[key]].append("N/A")
						self.timeline[self.lookup_dict[key]].append("N/A")
							
 
	def offload_to_file(self, path):
		f = open(path, 'w+')
		for key, value in self.timeline.items():
			str_out = key
			for n in value:
				str_out += (" " + str(n))
			str_out += "\n"
			f.write(str_out)

	def debug_print(self):
		print(self.lookup_dict)
		print(self.timeline)

def prefill_dict_from_lookup(lookup_path):
	reader = csv.reader(open(lookup_path))
	result = {}
	next(reader) #skip the header
	for row in reader:
		key = row[0] + '.0'
		result[key] = row[1]
	return result


def main():
	if len(sys.argv) != 2:
		print("Correct use: python3 createtimeline.py [subfolder with graphs]")
		sys.exit()
	path = "graphs/" + sys.argv[1] + "/"
	lookup_path = "lookup/test_lookup.txt"
	builder = TimelineBuilder(lookup_path, path)
	builder.build()
	builder.debug_print()
	builder.offload_to_file("text.txt")

if __name__ == "__main__":
	main()
