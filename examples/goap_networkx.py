import networkx as nx

G = nx.DiGraph()
goal = {'asg': True}
G.add_node(1, vpc=False)
G.add_node(2, vpn=False)
G.add_node(3, nat=False)
G.add_node(4, asg=False)
G.add_node(5, instance=False)
G.add_node(5, rds=False)
print(G.node[1])
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=1)
G.add_edge(2, 4, weight=1)
print(nx.astar_path(G, 1, 4))