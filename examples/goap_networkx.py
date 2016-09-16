import networkx as nx
from GOAP.Action import Actions

# settings
DEBUG = False

# ACTIONS
actions = Actions()
actions.add_action(
    name='CreateVPC',
    pre_conditions={'vpc': False, 'app': False, 'db': False},
    effects={'vpc': True, 'app': False, 'db': False}
)
actions.add_action(
    name='CreateDB',
    pre_conditions={'vpc': True, 'app': False, 'db': False},
    effects={'vpc': True, 'app': False, 'db': True}
)
actions.add_action(
    name='CreateApp',
    pre_conditions={'vpc': True, 'app': False, 'db': True},
    effects={'vpc': True, 'app': True, 'db': True}
)

# initial STATE
state = {'vpc': False, 'rds': False, 'db': False}

# GRAPH / World
G = nx.Graph()
G.add_node(0, attr_dict={'vpc': False, 'db': False, 'app': False})
G.add_node(1, attr_dict={'vpc': True, 'db': False, 'app': False})
G.add_node(2, attr_dict={'vpc': True, 'db': True, 'app': False})
G.add_node(3, attr_dict={'vpc': True, 'db': True, 'app': True})
# print(G.nodes(data=True))

# Test
for action in actions:
    # print(action)
    src = None
    dst = None
    obj = None
    for node in G.nodes(data=True):
        # print(node)
        # print(node[1])
        if action.pre_conditions == node[1]:
            src = node[0]
            if DEBUG:
                print('node data {0} = pre_conditions {2}'.format(node, node[1], action.pre_conditions))

        if action.effects == node[1]:
            dst = node[0]
            obj = action
            if DEBUG:
                print('Match! ', action.name)

        if src is not None and dst is not None:
            G.add_edge(src, dst, object=obj)
            if DEBUG:
                print('Edge created!')


print('Edges: ', G.edges(data=True))

