import networkx as nx


class Planner:
    """
    from Goap.Action import Actions

    # ACTIONS
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
    # Instantiate planner
    planner = Planner(
        actions=actions,
        init_state={'vpc': False, 'db': False, 'app': False},
        goal={'vpc': True, 'db': True, 'app': True}
    )
    print('Graph.Nodes: ', planner.graph.nodes(data=True))
    print('Graph.Edges: ', planner.graph.edges(data=True))
    print('Action sequence')
    pprint(planner.action_plan)
    # Plan again
    plan = planner.plan(
        init_state={'vpc': False, 'db': False, 'app': False},
        goal={'vpc': True, 'db': True, 'app': True}
    )
    plan = planner.plan(
        init_state={'vpc': True, 'db': False, 'app': False}, goal={'vpc': True, 'db': True, 'app': True})
    print('PATH: ', planner.path)
    print('Action sequence: ')
    pprint(plan, indent=2)

    Graph.Nodes:  [(0, {'db': False, 'app': False, 'vpc': False}), (1, {'db': False, 'app': False, 'vpc': True}), (2, {'db': True, 'app': False, 'vpc': True}), (3, {'db': 'started', 'app': False, 'vpc': True}), (4, {'db': 'stopped', 'app': False, 'vpc': True}), (5, {'db': 'not_health', 'app': False, 'vpc': True}), (6, {'db': True, 'app': True, 'vpc': True}), (7, {'db': True, 'app': 'stopped', 'vpc': True}), (8, {'db': True, 'app': 'started', 'vpc': True}), (9, {'db': True, 'app': 'not_health', 'vpc': True})]
    Graph.Edges:  [(0, 1, {'object': {"Conditions": {"db": false, "app": false, "vpc": false}, "Name": "CreateVPC", "Effects": {"db": false, "app": false, "vpc": true}}}), (1, 2, {'object': {"Conditions": {"db": false, "app": false, "vpc": true}, "Name": "CreateDB", "Effects": {"db": true, "app": false, "vpc": true}}}), (2, 6, {'object': {"Conditions": {"db": true, "app": false, "vpc": true}, "Name": "CreateApp", "Effects": {"db": true, "app": true, "vpc": true}}}), (3, 4, {'object': {"Conditions": {"db": "started", "app": false, "vpc": true}, "Name": "StopDB", "Effects": {"db": "stopped", "app": false, "vpc": true}}}), (4, 3, {'object': {"Conditions": {"db": "stopped", "app": false, "vpc": true}, "Name": "StartDB", "Effects": {"db": "started", "app": false, "vpc": true}}}), (5, 1, {'object': {"Conditions": {"db": "not_health", "app": false, "vpc": true}, "Name": "DestroyDB", "Effects": {"db": false, "app": false, "vpc": true}}}), (7, 8, {'object': {"Conditions": {"db": true, "app": "stopped", "vpc": true}, "Name": "StartApp", "Effects": {"db": true, "app": "started", "vpc": true}}}), (8, 7, {'object': {"Conditions": {"db": true, "app": "started", "vpc": true}, "Name": "StopApp", "Effects": {"db": true, "app": "stopped", "vpc": true}}}), (9, 2, {'object': {"Conditions": {"db": true, "app": "not_health", "vpc": true}, "Name": "DestroyApp", "Effects": {"db": true, "app": false, "vpc": true}}})]
    Action sequence
    [(0,
      1,
      {'object': {"Conditions": {"db": false, "app": false, "vpc": false}, "Name": "CreateVPC", "Effects": {"db": false, "app": false, "vpc": true}}}),
     (1,
      2,
      {'object': {"Conditions": {"db": false, "app": false, "vpc": true}, "Name": "CreateDB", "Effects": {"db": true, "app": false, "vpc": true}}}),
     (2,
      6,
      {'object': {"Conditions": {"db": true, "app": false, "vpc": true}, "Name": "CreateApp", "Effects": {"db": true, "app": true, "vpc": true}}})]
    PATH:  [1, 2, 6]
    Action plan:
    [ ( 1,
        2,
        { 'object': {"Conditions": {"db": false, "app": false, "vpc": true}, "Name": "CreateDB", "Effects": {"db": true, "app": false, "vpc": true}}}),
      ( 2,
        6,
        { 'object': {"Conditions": {"db": true, "app": false, "vpc": true}, "Name": "CreateApp", "Effects": {"db": true, "app": true, "vpc": true}}})]

    """

    def __init__(self, actions: object, init_state: dict, goal: dict) -> object:
        """
        :param actions: list of actions
        :param init_state: dict of initial state
        :param goal: dict of desired state
        """
        # init vars
        self.DEBUG = False
        self.nodes = None
        self.edges = None
        self.path = None
        self.action_plan = None
        # setup graph
        self.actions = actions
        self.graph = nx.DiGraph()
        self.init_state = init_state
        self.goal = goal
        # set nodes and edges and formulate plan
        self.set_nodes()
        self.set_edges()
        self.plan(init_state=init_state, goal=goal)

    def set_nodes(self):
        """

        :return: None
        """
        # states
        states = self.actions.all_possible_states()
        # generate graph from all_possible_states() method
        [self.graph.add_node(idx, attr_dict=state) for idx, state in enumerate(states)]
        self.nodes = self.graph.nodes(data=True)

    def set_edges(self):
        """

        :return: None
        """
        for action in self.actions.__iter__():
            src = None
            dst = None
            for node in self.nodes:
                if action.pre_conditions == node[1]:
                    src = node[0]
                if action.effects == node[1]:
                    dst = node[0]
                if src is not None and dst is not None:
                    self.graph.add_edge(src, dst, object=action)

        self.edges = self.graph.edges(data=True)

    def plan(self, init_state: dict, goal: dict) -> list:
        """

        :rtype: list
        :return: self.path
        """
        start_node = None
        final_node = None
        self.init_state = init_state
        self.goal = goal

        # find start and final node
        for node in self.nodes:
            if node[1] == self.init_state:
                start_node = node[0]
            elif self.goal == node[1]:
                final_node = node[0]

        self.path = nx.astar_path(self.graph, start_node, final_node)
        self.action_plan = self.graph.edges(self.path, data=True)

        return self.action_plan


if __name__ == '__main__':
    from Goap.Action import Actions
    from pprint import pprint

    # ACTIONS
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
    # Instantiate planner
    planner = Planner(
        actions=actions,
        init_state={'vpc': False, 'db': False, 'app': False},
        goal={'vpc': True, 'db': True, 'app': True}
    )
    print('Graph.Nodes: ', planner.graph.nodes(data=True))
    print('Graph.Edges: ', planner.graph.edges(data=True))
    print('Action sequence')
    pprint(planner.action_plan)
    # Plan again
    plan = planner.plan(
        init_state={'vpc': False, 'db': False, 'app': False},
        goal={'vpc': True, 'db': True, 'app': True}
    )
    plan = planner.plan(
        init_state={'vpc': True, 'db': False, 'app': False}, goal={'vpc': True, 'db': True, 'app': True})
    print('PATH: ', planner.path)
    print('Action plan: ')
    pprint(plan, indent=2)

