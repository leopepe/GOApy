import networkx as nx


class Planner:

    def __init__(self, actions: list, init_state: dict, goal: dict) -> object:
        """
        from GOAP.Action import Actions

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
        planner = Planner(actions, {'vpc': False, 'app': False, 'db': False}, {'vpc': True, 'app': True, 'db': True})
        plan = planner.plan()
        print(plan)
        [
            {
                'CreateVPC': {
                    'pre_conditions': {'app': False, 'vpc': False, 'db': False},
                    'effects': {'app': False, 'vpc': True, 'db': False}
                }
             },

            {
                'CreateDB': {
                    'pre_conditions': {'app': False, 'vpc': True, 'db': False},
                    'effects': {'app': False, 'vpc': True, 'db': True}
                }
            },

            {
                'CreateApp': {
                    'pre_conditions': {'app': False, 'vpc': True, 'db': True},
                    'effects': {'app': True, 'vpc': True, 'db': True}
                }
            }
        ]

        :param actions: list of actions
        :param init_state: dict of initial state
        :param goal: dict of desired state
        """
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

    def plan(self) -> list:
        """

        :return: List of Action objects needed to be executed to transit from initial state to goal
        """
        # get node index based on the node attr
        for node in self.graph.nodes(data=True):
            if node[1] == self.init_state:
                start = node[0]

        # get node index based on the node attr
        for node in self.graph.nodes(data=True):
            if node[1] == self.goal:
                final = node[0]

        path = nx.astar_path(self.graph, start, final)

        return [self.graph.get_edge_data(src, dst)['object'] for src, dst in self.graph.edges(path)]

if __name__ == '__main__':
    from GOAP.Action import Actions
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
    planner = Planner(actions, {'vpc': False, 'app': False, 'db': False}, {'vpc': True, 'app': True, 'db': True})
    plan = planner.plan()
    print(plan)
