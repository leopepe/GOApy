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

    def __init__(
            self,
            name,
            predecessor: Node,
            successor: Node,
            cost: float = 0.0,
            obj: object = None):
        self.name = name
        self.cost = cost
        self.predecessor = predecessor
        self.successor = successor
        self.obj = obj

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class Nodes(object):

    def __init__(self):
        self.nodes = []

    def __add__(self, other: Node):
        self.nodes.append(other)

    def __iter__(self):
        return iter(self.nodes)

    def add(self, other: Node):
        if other not in self.nodes:
            self.__add__(other)

    def get(self, attr):
        result = None
        for node in self.nodes:
            if node.attributes == attr:
                result = node
        return result


class Edges(object):

    def __init__(self, edges: list = None):
        if edges:
            for edge in edges:
                self.add(edge)
        else:
            self.edges = []

    def __add__(self, other: Edge):
        self.edges.append(other)

    def __iter__(self):
        return iter(self.edges)

    def add(self, other: Edge):
        self.__add__(other)


class Graph(object):
    def __init__(self, nodes: Nodes, edges: Edges):
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
        self.directed.add_node(
            node,
            attr_dict=attribute,
            label=node.name,
            object=node)

    def __add_edge(self, edge: Edge):
        self.directed.add_edge(
            edge.predecessor,
            edge.successor,
            object=edge.obj,
            weight=edge.cost,
            label=edge.name)

    def add_nodes_from(self, nodes: Nodes):
        [self.__add_node(node, attribute=node.attributes) for node in nodes]

    def add_edges_from(self, edges: Edges):
        [self.__add_edge(edge=edge) for edge in edges]

    def edge_between_nodes(self, path: list, data: bool = True):
        return self.directed.edges(path, data=data)

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
            return nx.astar_path(self.directed, src, dst)

    def plot(self, file_path: str):
        try:
            import matplotlib.pyplot as plt
        except ImportError as err:
            raise ImportError(f'matplotlib not installed. Failed at: {err}')

        try:
            pos = nx.nx_agraph.graphviz_layout(self.directed)
            nx.draw(
                self.directed,
                pos=pos,
                node_size=1200,
                node_color='lightblue',
                linewidths=0.25,
                font_size=8,
                font_weight='bold',
                with_labels=True,
                dpi=5000
            )
            # edge_labels = nx.get_edge_attributes(self.directed, name='attr_dict')
            # nx.draw_networkx_edge_labels(self.directed, pos=pos, edge_labels=edge_labels)
            plt.savefig(file_path)
        except IOError as err:
            raise IOError(f'Could not create plot image: {err}')


class Planner(object):

    def __init__(self, actions: Actions):
        """
        :param actions: list of actions
        """
        # init vars
        self.goal = None
        self.world_state = None
        self.actions = actions
        self.states = Nodes()
        self.transitions = Edges()
        self.action_plan = []
        self.graph = Graph(nodes=self.states, edges=self.transitions)

    def __generate_states(self, actions: Actions, world_state: dict, goal: dict):
        self.states.add(Node(world_state))
        self.states.add(Node(goal))
        for action in actions:
            pre = {**world_state, **action.pre_conditions}
            eff = {**pre, **action.effects}
            self.states.add(Node(attributes=pre))
            self.states.add(Node(attributes=eff))

    def __generate_transitions(self, actions, states):
        for action in actions:
            for state in states:
                if action.pre_conditions.items() <= state.attributes.items():
                    attr = {**state.attributes, **action.effects}
                    suc = self.states.get(attr)
                    self.transitions.add(
                        Edge(
                            name=action.name,
                            predecessor=state,
                            successor=suc,
                            cost=action.cost,
                            obj=action))

    def plan(self, state: dict, goal: dict) -> list:
        self.world_state = state
        self.goal = goal
        self.__generate_states(self.actions, self.world_state, self.goal)
        self.__generate_transitions(self.actions, self.states)
        self.graph = Graph(self.states, self.transitions)
        ws_node = self.states.get(state)
        gs_node = self.states.get(goal)
        plan = []
        if state != goal:
            try:
                path = self.graph.path(ws_node, gs_node)
            except EnvironmentError as e:
                print(f"No possible path: {e}")

            try:
                plan = self.graph.edge_between_nodes(path)
            except EnvironmentError as e:
                print(f"No plan available: {e}")

        return plan
