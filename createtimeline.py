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

	def debug_print(self):
		print(self.lookup_dict)

def prefill_dict_from_lookup(lookup_path):
	reader = csv.reader(open(lookup_path))
	result = {}
	next(reader) #skip the header
	for row in reader:
		key = row[0]
		result[key] = row[1:]
	return result


def main():
	if len(sys.argv) != 2:
		print("Correct use: python3 createtimeline.py [subfolder with graphs]")
		sys.exit()
	path = "graphs/" + sys.argv[1]
	testfiles = os.listdir(path)
	timeline = defaultdict(list)  # using dictionary of lists to store {["Name of the city"], [list of the values]}
	lookup_path = "lookup/test_lookup.txt"
	builder = TimelineBuilder(lookup_path, path)
	builder.debug_print()

if __name__ == "__main__":
	main()
