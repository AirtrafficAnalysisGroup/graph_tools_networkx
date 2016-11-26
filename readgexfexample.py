import networkx as nx

G=nx.read_gexf("graphs/test.gexf")
print(G.nodes(data=True))
print(G.edges(data=True))
