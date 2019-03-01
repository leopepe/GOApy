from Goap.WorldState import WorldState
from Goap.Action import Actions
import networkx as nx


class Node(object):

    def __init__(self, attributes: dict, weight: float = 0.0):
        self.attributes = attributes
        self.weight = weight
        self.name = str(self.attributes)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Edge(object):

    def __init__(self, name, predecessor: Node, successor: Node, cost: float = 0.0):
        self.name = name
        self.cost = cost
        self.predecessor = predecessor
        self.successor = successor

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Graph(object):
    def __init__(self, nodes: list, edges: list):
        self.directed = nx.DiGraph()
        self.add_nodes_from(nodes=nodes)
        self.add_edges_from(edges=edges)
        self.__size = self.size

    def __repr__(self):
        return self.directed

    @staticmethod
    def __is_dst(src: dict, dst: dict) -> bool:
        if src == dst:
            return True
        else:
            return False

    @property
    def size(self):
        return len(self.directed.nodes)

    def __add_node(self, node: Node, attribute: dict):
        self.directed.add_node(node, attr_dict=attribute, label=node.name, object=node)

    def __add_edge(self, edge: Edge):
        self.directed.add_edge(edge.predecessor, edge.successor, object=edge, weight=edge.cost, label=edge.name)

    def add_nodes_from(self, nodes: list):
        [self.__add_node(node, attribute=node.attributes) for node in nodes]

    def add_edges_from(self, edges: list):
        [self.__add_edge(edge=edge) for edge in edges]

    def edge_between_nodes(self, src: str, dst: str, data: bool = True):
        return self.directed.edges(nbunch=(src, dst), data=data)

    def nodes(self, data: bool = True):
        return self.directed.nodes(data=data)

    def edges(self, data: bool = True):
        return self.directed.edges(data=data)

    def search_node(self, attr: dict = None):
        result = None
        if attr:
            for node in self.directed.nodes(data=True):
                if node[1]['attr_dict'].items() == attr.items():
                    result = node[0]
        return result

    def path(self, src: dict, dst: dict):
        if not self.__is_dst(src, dst):
            return nx.astar_path(self.directed, self.search_node(attr=src), self.search_node(attr=dst))

    def plot(self, file_path: str):
        try:
            import matplotlib.pyplot as plt
        except ImportError as err:
            raise('matplotlib not installed. Failed at: {}', err)

        try:
            pos = nx.nx_agraph.graphviz_layout(self.directed)
            nx.draw(
                self.directed,
                pos=pos,
                node_size=1200,
                node_color='lightblue',
                linewidths=0.25,
                font_size=10,
                font_weight='bold',
                with_labels=True,
                dpi=1000
            )
            plt.savefig(file_path)
        except IOError as err:
            raise('Could not create plot image: {}', err)


class Planner(object):

    def __init__(self, world_state: WorldState, actions: Actions):
        """
        :param actions: list of actions
        """
        # init vars
        self.world_state = world_state
        self.actions = actions
        self.states = self.__generate_states(self.actions, self.world_state)
        self.transitions = self.__generate_transitions(self.actions, self.states)
        self.action_plan = []
        self.graph = Graph(nodes=self.states, edges=self.transitions)

    @staticmethod
    def __isinlist(dic: dict, l: list):
        for d in l:
            if dic == d:
                return True
        return False

    @staticmethod
    def to_str(dic):
        return str(dic).replace('\'', '')

    def __generate_states(self, actions, world_state):
        states = []
        if not states:
            states.append(Node(attributes=world_state))

        for action in actions:
            pre = {**world_state, **action.pre_conditions}
            eff = {**world_state, **action.effects}
            if not self.__isinlist(pre, states):
                states.append(Node(attributes=pre))
            if not self.__isinlist(eff, states):
                states.append(Node(attributes=eff))
        return states

    @staticmethod
    def __generate_transitions(actions, states):
        edges = []
        pre, suc = None, None
        for state in states:
            for action in actions:
                if action.pre_conditions.items() <= state.attributes.items():
                    pre = state
                if action.effects.items() <= state.attributes.items():
                    suc = state
                if pre and suc:
                    edges.append(Edge(name=action.name, predecessor=pre, successor=suc, cost=action.cost))
                    pre, suc = None, None
        return edges

    @staticmethod
    def __is_end(i: int, l: list) -> bool:
        if i == len(l) - 1:
            return True
        else:
            return False

    def plan(self, state: dict, goal: dict) -> list:
        plan = []
        if state != goal:
            path = self.graph.path(state, goal)
            plan = self.graph.edge_between_nodes(path[0], path[1])
        return plan


if __name__ == '__main__':
    # constants
    init_ws = WorldState(lv_need_expansion=False, vg_need_expansion=False)
    ws = WorldState(lv_need_expansion=True, vg_need_expansion=True)
    gs = WorldState(lv_need_expansion=False, vg_need_expansion=False)
    #
    acts = Actions()
    acts.add(
        name='ExpandLV',
        pre_conditions={
            'lv_need_expansion': True,
            'vg_need_expansion': False,
        },
        effects={
            'lv_need_expansion': False,
        },
        shell='echo expand_lv',
        cost=1.0
    )
    acts.add(
        name='ExpandVG',
        pre_conditions={
            'vg_need_expansion': True,
        },
        effects={
            'vg_need_expansion': False,
        },
        shell='echo expand_vg'
    )
    acts.add(
        name='PurgeOldFiles',
        pre_conditions={
            'lv_need_expansion': True,
            'vg_need_expansion': True,
        },
        effects={
            'lv_need_expansion': False,
        },
        shell='echo purge_old_files',
        cost=1.5,
    )
    p = Planner(world_state=init_ws, actions=acts)
    p.graph.plot('graph.png')
    print(p.graph.nodes(data=True))
    print(p.graph.size)
    print(p.graph.edges(data=True))
    # for n in p.graph.nodes(data=True):
    #     print(n)
    # print(world_state)
    # print(p.graph.edge_between_nodes(src='{lv_state: out_of_capacity, vg_state: ok}', dst='{lv_state: ok}'))
    print(p.graph.path(ws, gs))
    print(p.plan(ws, gs))
    # print(gs)
    # print(p.graph.get_node(gs))
