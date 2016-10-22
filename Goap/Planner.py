import networkx as nx


class Planner:
    """
        from Goap.Action import Actions

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
    """

    def __init__(self, actions: object, init_state: dict, goal: dict) -> object:
        """
        :param actions: list of actions
        :param init_state: dict of initial state
        :param goal: dict of desired state
        """
        self.DEBUG = False
        self.nodes = None
        self.edges = None
        self.path = None
        self.graph = nx.DiGraph()
        self.actions = actions
        self.init_state = init_state
        self.goal = goal
        self.set_nodes()
        self.set_edges()

    def set_nodes(self):
        """

        :return: None
        """
        i = 0
        for action in self.actions:
            self.graph.add_node(i, attr_dict=action.pre_conditions)
            i += 1

            if i == len(self.actions):
                self.graph.add_node(i, attr_dict=action.effects)

            if self.DEBUG:
                print('pre-condition: {0}, counter: {1}'.format(action.pre_conditions, i))

        self.nodes = self.graph.nodes(data=True)
        return self.nodes

    def set_edges(self):
        """

        :return: None
        """
        # Test
        for action in self.actions:
            # print(action)
            src = None
            dst = None
            obj = None
            for node in self.graph.nodes(data=True):
                if action.pre_conditions == node[1]:
                    src = node[0]

                if action.effects == node[1]:
                    dst = node[0]
                    obj = action

                if src is not None and dst is not None:
                    self.graph.add_edge(src, dst, object=obj)

                if self.DEBUG:
                    print('DST node data {0} = effects {2}'.format(node, node[1], action.effects))
                    print('SRC node data {0} = pre_conditions {2}'.format(node, node[1], action.pre_conditions))

        self.edges = self.graph.edges(data=True)
        return self.edges

    def plan(self, init_state: dict=None, goal: dict=None) -> list:
        """

        :rtype: list
        :return: Action's object collection. All action objects needed to execute the plan
        """
        start_node = None
        final_node = None
        path = None
        if init_state:
            self.init_state = init_state

        if goal:
            self.goal = goal

        # get node index based on the node attr
        for node in self.graph.nodes(data=True):
            if node[1] == self.init_state:
                start_node = node[0]
                # print(start_node)

        # get node index based on the node attr
        for node in self.graph.nodes(data=True):
            if node[1] == self.goal:
                final_node = node[0]
                # print(final_node)

        self.path = nx.astar_path(self.graph, start_node, final_node)
        return [self.graph.get_edge_data(src, dst)['object'] for src, dst in self.graph.edges(self.path)]

if __name__ == '__main__':
    from Goap.Action import Actions
    actions = Actions()
    actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
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
    planner = Planner(
        actions=actions,
        init_state={'vpc': False, 'db': False, 'app': False},
        goal={'vpc': True, 'db': True, 'app': True}
    )
    plan = planner.plan()
    print(planner.path)
    print(planner.graph.nodes(data=True))
    print(planner.graph.edges(data=True))
    print(planner.graph.edges(planner.path))
    print(len(planner.graph.edges(planner.path)))
    print('plan: ', plan)
    # print('plan: {0}, type: {1}, nodes: {2}, edges: {3}'.format(plan, type(plan), planner.nodes, planner.edges))

    print('###############')
    planner2 = Planner(
        actions=actions,
        init_state={'vpc': True, 'app': False, 'db': False},
        goal={'vpc': True, 'app': True, 'db': True}
    )
    plan2 = planner2.plan(
        init_state={'vpc': True, 'app': False, 'db': False},
        goal={'vpc': True, 'app': True, 'db': True}
    )
    print(planner2.path)
    print(planner2.graph.nodes(data=True))
    print(planner2.graph.edges(data=True))
    print(planner2.graph.edges(planner2.path))
    print(len(planner2.graph.edges(planner2.path)))
    print('plan: ', plan2)
    # print('plan: {0}, type: {1}, nodes: {2}, edges: {3}'.format(plan2, type(plan2), planner2.nodes, planner2.edges))
