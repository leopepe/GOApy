import networkx as nx
from Goap.Action import Actions

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
    pre_conditions={'vpc': True, 'db': False, 'app': False},
    effects={'vpc': True, 'db': True, 'app': False}
)
actions.add_action(
    name='CreateApp',
    pre_conditions={'vpc': True, 'db': True, 'app': False},
    effects={'vpc': True, 'db': True, 'app': True}
)

# initial STATE
initial_state = ({'vpc': False}, {'db': False}, {'app': False})

# goal
goal = ({'vpc': True}, {'db': True}, {'app': True})

# GRAPH / World
G = nx.DiGraph()
# G.add_node(0, attr_dict={'vpc': False, 'db': False, 'app': False})
# G.add_node(1, attr_dict={'vpc': True, 'db': False, 'app': False})
# G.add_node(2, attr_dict={'vpc': True, 'db': True, 'app': False})
# G.add_node(3, attr_dict={'vpc': True, 'db': True, 'app': True})
# print(G.nodes(data=True))
"""
i = 0
for action in actions:
    G.add_node(i, attr_dict=action.pre_conditions)
    if DEBUG:
        print('AUTO Conditions: {0}, i: {1}'.format(action.pre_conditions, i))
    i += 1

    if i == len(actions):
        G.add_node(i, attr_dict=action.effects)

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
                print('SRC node data {0} = pre_conditions {2}'.format(node, node[1], action.pre_conditions))

        if action.effects == node[1]:
            dst = node[0]
            obj = action
            if DEBUG:
                print('DST node data {0} = effects {2}'.format(node, node[1], action.effects))

        if src is not None and dst is not None:
            G.add_edge(src, dst, object=obj)
            if DEBUG:
                print('Edge created!')

# search
#
#
for node in G.nodes(data=True):
    if node[1] == initial_state:
        start = node[0]

# final
for node in G.nodes(data=True):
    if node[1] == goal:
        final = node[0]

# path = nx.astar_path(G, start, goal)
path = nx.astar_path(G=G, source=start, target=final)
print(path)

# list actions to achive goal
print(G.edges(path))
for src, dst in G.edges(path):
    print(G.get_edge_data(src,dst))

print('Edges: ', G.edges(data=True))
"""
from Goap.Action import Actions
from pprint import pprint

actions = Actions()
# VPC/Network set
actions.add_action(
    name='CreateVPC',
    pre_conditions={'vpc': False, 'db': False, 'app': False},
    effects={'vpc': True, 'db': False, 'app': False}
)
# DB set
actions.add_action(
    name='CreateDB',
    pre_conditions={'vpc': True, 'db': False, 'app': False},
    effects={'vpc': True, 'db': True, 'app': False}
)
actions.add_action(
    name='StopDB',
    pre_conditions={'vpc': True, 'db': 'started', 'app': False},
    effects={'vpc': True, 'db': 'stopped', 'app': False}
)
actions.add_action(
    name='StartDB',
    pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
    effects={'vpc': True, 'db': 'started', 'app': False}
)
actions.add_action(
    name='DestroyDB',
    pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
    effects={'vpc': True, 'db': False, 'app': False}
)
# APP set
actions.add_action(
    name='CreateApp',
    pre_conditions={'vpc': True, 'db': True, 'app': False},
    effects={'vpc': True, 'db': True, 'app': True}
)
actions.add_action(
    name='StartApp',
    pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
    effects={'vpc': True, 'db': True, 'app': 'started'}
)
actions.add_action(
    name='StopApp',
    pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
    effects={'vpc': True, 'db': True, 'app': 'stopped'}
)
actions.add_action(
    name='DestroyApp',
    pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
    effects={'vpc': True, 'db': True, 'app': False}
)
# states
states = actions.all_possible_states()
# generate states grid
g = nx.DiGraph()
# generate graph from all_possible_states() method
[g.add_node(idx, attr_dict=state) for idx, state in enumerate(states)]

nodes = g.nodes(data=True)
pprint(g.nodes(data=True), indent=2)

# set edges
for action in actions:
    src = None
    dst = None
    for node in nodes:
        obj = action
        if action.pre_conditions == node[1]:
            src = node[0]
        if action.effects == node[1]:
            dst = node[0]
        if src is not None and dst is not None:
            g.add_edge(src, dst, object=obj)

pprint(g.edges(data=True), indent=2)
pprint(g.get_edge_data(0, 1), indent=2)
