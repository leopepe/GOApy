import networkx as nx


class Planner:

    def __init__(self, actions, init_state, goal):
        self.graph = nx.Graph()
        self.actions = actions
        self.init_state = init_state
        self.goal = goal
        self.DEBUG = False
        self.set_nodes()
        self.set_edges()

    def set_nodes(self):
        i = 0
        for action in self.actions:
            self.graph.add_node(i, attr_dict=action.pre_conditions)
            if self.DEBUG:
                print('AUTO Conditions: {0}, i: {1}'.format(action.pre_conditions, i))
            i += 1

            if i == len(self.actions):
                self.graph.add_node(i, attr_dict=action.effects)

    def set_edges(self):
        # Test
        for action in self.actions:
            # print(action)
            src = None
            dst = None
            obj = None
            for node in self.graph.nodes(data=True):
                if action.pre_conditions == node[1]:
                    src = node[0]
                    if self.DEBUG:
                        print('SRC node data {0} = pre_conditions {2}'.format(node, node[1], action.pre_conditions))

                if action.effects == node[1]:
                    dst = node[0]
                    obj = action
                    if self.DEBUG:
                        print('DST node data {0} = effects {2}'.format(node, node[1], action.effects))

                if src is not None and dst is not None:
                    self.graph.add_edge(src, dst, object=obj)
                    if self.DEBUG:
                        print('Edge created!')

    def plan(self):
        # get node index based on the node attr
        for node in self.graph.nodes(data=True):
            if node[1] == self.init_state:
                start = node[0]

        for node in self.graph.nodes(data=True):
            if node[1] == goal:
                final = node[0]

        path = nx.astar_path(self.graph, start, final)

        return [self.graph.get_edge_data(src, dst) for src, dst in self.graph.edges(path)]

if __name__ == '__main__':
    planner = Planner()