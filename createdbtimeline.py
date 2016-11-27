import sqlite3
import networkx as nx

G=nx.read_gexf("graphs/test.gexf")

conn = sqlite3.connect('database/test.db')

c = conn.cursor()

c.execute('CREATE TABLE airports (id REAL PRIMARY KEY NOT NULL, market_id REAL NOT NULL, in_degree_people REAL, out_degree_people REAL, in_degree_fare REAL, out_degree_fare REAL, year INT);')

conn.commit()

for node,data in G.nodes_iter(data=True):
	in_peop = G.in_degree(node, weight='num_of_people')
	out_peop = G.out_degree(node, weight='num_of_people')
	in_price = G.in_degree(node, weight='total_price')
	out_price = G.out_degree(node, weight='total_price')
	year = 2014 #fix later
	market_id = data['market_id']
	row = (node, market_id, in_peop, out_peop, in_price, out_price, year)
	print(row)
	c.execute('INSERT INTO airports VALUES (?,?,?,?,?,?,?)', row)

print('Now trying to get stuff out')

for row in c.execute('SELECT * FROM airports ORDER BY in_degree_people'):
	print(row) 

conn.close()

