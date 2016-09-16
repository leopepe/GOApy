from collections import deque
import networkx as nx


class Plan:

    def __init__(self):
        self.steps = deque()

    def put(self, action):
        self.steps.append(action)

    def get(self, action):
        self.steps.pop(action)

    def empty(self):
        return len(self.steps) == 0

    def __str__(self):
        return '{0}, NSteps: {1}, Steps: {2}'.format(self.__class__, len(self.steps), self.steps)

    def __repr__(self):
        return self.__str__()


class Planner:

    def __init__(self, actions, initial_state):
        self.graph = nx.Graph()
        self.actions = actions
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

    def search(self, ):


if __name__ == '__main__':
    pass