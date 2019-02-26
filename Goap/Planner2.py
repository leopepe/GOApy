from Goap.Action import Actions, Action
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

    def __repr__(self):
        return self.directed

    @staticmethod
    def __is_dst(src: dict, dst: dict) -> bool:
        if src == dst:
            return True
        else:
            return False

    def __add_node(self, node: Node, attribute: dict):
        # self.directed.add_node(node, attr_dict=attribute, label=self.to_str(attribute))
        self.directed.add_node(node, attr_dict=attribute, label=node.name)

    def __add_edge(self, edge: Edge):
        self.directed.add_edge(edge.predecessor, edge.successor, object=edge, weight=edge.cost, label=edge.name)

    def add_nodes_from(self, nodes: list):
        [self.__add_node(node, attribute=node.attributes) for node in nodes]

    def add_edges_from(self, edges: list):
        [self.__add_edge(edge=edge) for edge in edges]

    def nodes(self, data: bool = True):
        return self.directed.nodes(data=data)

    def edges(self, data: bool = True):
        return self.directed.edges(data=data)

    def edge_between_nodes(self, src: str, dst: str):
        return self.directed.edges(nbunch=(src, dst), data=True)

    def path(self, src: dict, dst: dict):
        if not self.__is_dst(src, dst):
            origin = self.get_node(attr=src)
            goal = self.get_node(attr=dst)
            return nx.astar_path(self.directed, self.get_node(attr=src), self.get_node(attr=dst))

    def get_node(self, index: int = None, attr: dict = None):
        print('attr ', attr)
        # print(self.directed.nodes(data=True))
        if index:
            for node in self.directed.nodes(data=True):
                if node[0] == index:
                    return node
                else:
                    return 'NotFound'
        elif attr:
            for node in self.directed.nodes(data=True):
                print(node[1]['attr_dict'])
                if node[1]['attr_dict'] == attr:
                    # print('found ', node[1])
                    return node
                else:
                    print('fdp de node ', node[1]['attr_dict'])
                    return 'NotFound'

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

    def __init__(self, ws: dict, actions: Actions):
        """
        :param actions: list of actions
        """
        # init vars
        self.DEBUG = False
        self.world_state = ws
        self.actions = actions
        self.states = self.__generate_states(actions)
        self.transitions = self.__generate_transitions(actions, self.states)
        self.action_plan = []
        self.graph = Graph(nodes=self.states, edges=self.transitions)

    @staticmethod
    def to_str(dic):
        return str(dic).replace('\'', '')

    @staticmethod
    def __generate_states(actions):
        states = []
        for action in actions:
            if action.pre_conditions not in states:
                states.append(Node(attributes=action.pre_conditions))
            if action.effects not in states:
                states.append(Node(attributes=action.effects))
        return states

    @staticmethod
    def __generate_transitions(actions, states):
        edges = []
        pre = None
        suc = None
        for action in actions:
            for state in states:
                if action.pre_conditions.items() <= state.attributes.items():
                    pre = state
                if action.effects.items() <= state.attributes.items():
                    suc = state
            if pre and suc:
                edges.append(Edge(name=action.name, predecessor=pre, successor=suc, cost=action.cost))
        return edges

    @staticmethod
    def __is_end(i: int, l: list) -> bool:
        if i == len(l) - 1:
            return True
        else:
            return False

    def plan(self, state: dict, goal: dict) -> list:
        pass


if __name__ == '__main__':
    world_state = {
        'lv_need_expansion': True,
        'vg_need_expansion': False,
        'has_files_to_purge': False
    }
    goal = {
        'lv_need_expansion': False,
        'vg_need_expansion': False,
        'has_files_to_purge': False
    }
    actions = Actions()
    actions.add(
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
    actions.add(
        name='ExpandVG',
        pre_conditions={
            'vg_need_expansion': True,
        },
        effects={
            'vg_need_expansion': False,
        },
        shell='echo expand_vg'
    )
    actions.add(
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
    p = Planner(ws=world_state, actions=actions)
    p.graph.plot('graph.png')
    print(p.graph.nodes(data=True))
    # print(len(p.graph.nodes()))
    print(p.graph.edges(data=True))
    # for n in p.graph.nodes(data=True):
    #     print(n)
    # print(p.actions_attributes(std_world_state, actions))
    # print(world_state)
    # print(p.graph.edge_between_nodes(src='{lv_state: out_of_capacity, vg_state: ok}', dst='{lv_state: ok}'))
    # print(p.graph.path(world_state, goal))
    # print(p.plan(world_state, goal))
