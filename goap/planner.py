# -*- coding: utf-8 -*-
"""
 planner.py

"""
import networkx as nx

from goap.action import Actions
from goap.errors import PlanFailed


class Planner:
    """Usage: from goap.Action import Actions

    # ACTIONS actions = Actions() # VPC/Network set actions.add_action(

        name='CreateVPC', pre_conditions={'vpc': False, 'db': False, 'app':
        False}, effects={'vpc': True, 'db': False, 'app': False}

    ) # DB set actions.add_action(

        name='CreateDB', pre_conditions={'vpc': True, 'db': False, 'app':
        False}, effects={'vpc': True, 'db': True, 'app': False}

    ) actions.add_action(

        name='StopDB', pre_conditions={'vpc': True, 'db': 'started', 'app':
        False}, effects={'vpc': True, 'db': 'stopped', 'app': False}

    ) actions.add_action(

        name='StartDB', pre_conditions={'vpc': True, 'db': 'stopped', 'app':
        False}, effects={'vpc': True, 'db': 'started', 'app': False}

    ) actions.add_action(

        name='DestroyDB', pre_conditions={'vpc': True, 'db': 'not_health',
        'app': False}, effects={'vpc': True, 'db': False, 'app': False}

    ) # APP set actions.add_action(

        name='CreateApp', pre_conditions={'vpc': True, 'db': True, 'app':
        False}, effects={'vpc': True, 'db': True, 'app': True}

    ) actions.add_action(

        name='StartApp', pre_conditions={'vpc': True, 'db': True, 'app':
        'stopped'}, effects={'vpc': True, 'db': True, 'app': 'started'}

    ) actions.add_action(

        name='StopApp', pre_conditions={'vpc': True, 'db': True, 'app':
        'started'}, effects={'vpc': True, 'db': True, 'app': 'stopped'}

    ) actions.add_action(

        name='DestroyApp', pre_conditions={'vpc': True, 'db': True, 'app':
        'not_health'}, effects={'vpc': True, 'db': True, 'app': False}

    ) # Instantiate planner planner = Planner(

        actions=actions, init_state={'vpc': False, 'db': False, 'app': False},
        goal={'vpc': True, 'db': True, 'app': True}

    ) print('Graph.Nodes: ', planner.graph.nodes(data=True))
    print('Graph.Edges: ', planner.graph.edges(data=True)) print('Action
    sequence') pprint(planner.action_plan) # Plan again planning =
    planner.planning(

        init_state={'vpc': False, 'db': False, 'app': False}, goal={'vpc': True,
        'db': True, 'app': True}

    ) planning = planner.planning(

        init_state={'vpc': True, 'db': False, 'app': False}, goal={'vpc': True,
        'db': True, 'app': True})

    print('PATH: ', planner.path) print('Action sequence: ') pprint(planning,
    indent=2)

    Graph.Nodes: [(0, {'db': False, 'app': False, 'vpc': False}), (1, {'db':
    False, 'app': False, 'vpc': True}), (2, {'db': True, 'app': False, 'vpc':
    True}), (3, {'db': 'started', 'app': False, 'vpc': True}), (4, {'db':
    'stopped', 'app': False, 'vpc': True}), (5, {'db': 'not_health', 'app':
    False, 'vpc': True}), (6, {'db': True, 'app': True, 'vpc': True}), (7,
    {'db': True, 'app': 'stopped', 'vpc': True}), (8, {'db': True, 'app':
    'started', 'vpc': True}), (9, {'db': True, 'app': 'not_health', 'vpc':
    True})] Graph.Edges: [(0, 1, {'object': {"Conditions": {"db": false, "app":
    false, "vpc": false}, "Name": "CreateVPC", "Effects": {"db": false, "app":
    false, "vpc": true}}}), (1, 2, {'object': {"Conditions": {"db": false,
    "app": false, "vpc": true}, "Name": "CreateDB", "Effects": {"db": true,
    "app": false, "vpc": true}}}), (2, 6, {'object': {"Conditions": {"db": true,
    "app": false, "vpc": true}, "Name": "CreateApp", "Effects": {"db": true,
    "app": true, "vpc": true}}}), (3, 4, {'object': {"Conditions": {"db":
    "started", "app": false, "vpc": true}, "Name": "StopDB", "Effects": {"db":
    "stopped", "app": false, "vpc": true}}}), (4, 3, {'object': {"Conditions":
    {"db": "stopped", "app": false, "vpc": true}, "Name": "StartDB", "Effects":
    {"db": "started", "app": false, "vpc": true}}}), (5, 1, {'object':
    {"Conditions": {"db": "not_health", "app": false, "vpc": true}, "Name":
    "DestroyDB", "Effects": {"db": false, "app": false, "vpc": true}}}), (7, 8,
    {'object': {"Conditions": {"db": true, "app": "stopped", "vpc": true},
    "Name": "StartApp", "Effects": {"db": true, "app": "started", "vpc":
    true}}}), (8, 7, {'object': {"Conditions": {"db": true, "app": "started",
    "vpc": true}, "Name": "StopApp", "Effects": {"db": true, "app": "stopped",
    "vpc": true}}}), (9, 2, {'object': {"Conditions": {"db": true, "app":
    "not_health", "vpc": true}, "Name": "DestroyApp", "Effects": {"db": true,
    "app": false, "vpc": true}}})] Action sequence [(0,

            1, {'object': {"Conditions": {"db": false, "app": false, "vpc":
            false}, "Name": "CreateVPC", "Effects": {"db": false, "app": false,
            "vpc": true}}}),

        (1,
            2, {'object': {"Conditions": {"db": false, "app": false, "vpc":
            true}, "Name": "CreateDB", "Effects": {"db": true, "app": false,
            "vpc": true}}}),

        (2,
            6, {'object': {"Conditions": {"db": true, "app": false, "vpc":
            true}, "Name": "CreateApp", "Effects": {"db": true, "app": true,
            "vpc": true}}})]

    PATH: [1, 2, 6] Action planning: [ ( 1,

            2, { 'object': {"Conditions": {"db": false, "app": false, "vpc":
            true}, "Name": "CreateDB", "Effects": {"db": true, "app": false,
            "vpc": true}}}),

        ( 2,
            6, { 'object': {"Conditions": {"db": true, "app": false, "vpc":
            true}, "Name": "CreateApp", "Effects": {"db": true, "app": true,
            "vpc": true}}})]
    """

    def __init__(self, actions: Actions, init_state: dict = {}, goal: dict = {}):
        """
        Args:
            actions (Actions): list of actions
            init_state (dict): dict of initial state
            goal (dict): dict of desired state
        """
        # init vars
        self.debug = False
        self.nodes = None
        self.edges = None
        self.path = None
        self.action_plan = []
        # setup graph
        self.actions = actions
        self.graph = nx.DiGraph()
        self.init_state = init_state
        self.goal = goal
        # set nodes and edges and formulate planning
        self.set_nodes()
        self.set_edges()
        self.plan(init_state=init_state, goal=goal)

    @staticmethod
    def __idx_is_end_node(i: int, _l: list) -> bool:
        """
        Args:
            i (int):
            _l (list):
        """
        return i == len(_l) - 1

    def set_nodes(self):
        """
        Returns:
            None
        """
        states = self.actions.all_possible_states()
        # add nodes (idx: int, state: dict)
        [self.graph.add_node(idx, attr_dict=state) for idx, state in enumerate(states)]
        self.nodes = self.graph.nodes(data=True)

    def set_edges(self):
        """
        Todo:
            test:
                superset = node[1] subnet = preconditions, effects if all(item
                in superset.items() for item in subset.items())

        Returns:
            None
        """
        # for action in self.actions.__iter__():
        for action in self.actions:
            src = None
            dst = None
            for node in self.nodes:
                if action.pre_conditions == node[1]:
                    src = node[0]
                if action.effects == node[1]:
                    dst = node[0]

                if src is not None and dst is not None:
                    self.graph.add_edge(src, dst, object=action)
                    src = None
                    dst = None

        self.edges = self.graph.edges(data=True)

    def plan(self, init_state: dict, goal: dict) -> list:
        """
        Args:
            init_state (dict):
            goal (dict):

        Returns:
            list: self.path
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
        # Try to generate the plan, return False if fails
        try:
            self.path = nx.astar_path(self.graph, start_node, final_node)
            for idx, i in enumerate(self.path):
                if self.__idx_is_end_node(idx, self.path):
                    break
                else:
                    current = i
                    nxt = self.path[idx + 1]
                    # planning.append(self.graph.in_edges(nbunch=(current, nxt), data=True))
                    for src, dst, data in self.graph.edges(data=True):
                        if (current, nxt) == (src, dst):
                            self.action_plan.append((src, dst, data))
            # commented to include the for above
            # self.action_plan = self.graph.edges(self.path, data=True)
            return self.action_plan
        except PlanFailed as plan_failed_exception:
            print('[ERROR] There is no node to start planning {}'.format(plan_failed_exception))
            return []

    def plot_graph(self, file_name: str = 'graph.png', label_nodes: bool = True, label_edges: bool = True):
        """
        Args:
            file_name (str):
            label_nodes (bool):
            label_edges (bool):
        """
        import matplotlib.pyplot as plt
        # pos = nx.spring_layout(self.graph)
        pos = nx.shell_layout(self.graph, dim=1024, scale=0.5)
        # pos = nx.random_layout(self.graph, dim=1024, scale=0.5)

        if label_edges:
            edge_labels = {
                (edge[0], edge[1]): edge[2]['object'] for edge in self.graph.edges(data=True)
            }
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=5)

        if label_nodes:
            labels = {node[0]: node[1] for node in self.graph.nodes(data=True)}
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=5, alpha=0.8)

        # nx.draw(self.graph, with_labels=True, arrows=True, node_size=80)
        nx.draw_spectral(self.graph, with_labels=True, arrows=True, node_size=80)
        plt.savefig(file_name, dpi=1024)


if __name__ == '__main__':
    from goap.action import Actions
    from pprint import pprint

    # ACTIONS
    fs_actions = Actions()
    fs_actions.add(
        name='CompactBigLogFiles',
        pre_conditions={'files_to_compact': 'Exists'},
        effects={'files_to_compact': 'None'},
        shell='find /tmp -name "*.log" -type f -size +900M| xargs tar -zcvf logfile-$(date "+%d%m%y-%H%M%S").tar.gz {}'
    )
    print(fs_actions)
    print('Actions: ', fs_actions)
    planner = Planner(actions=fs_actions)
    print('Planner: ', planner)
    print('Graph.Nodes: ', planner.graph.nodes(data=True))
    print('Graph.Edges: ', planner.graph.edges(data=True))
    print('Action sequence')
    # Plan again
    plan = planner.plan(
        init_state={'files_to_compact': 'Exists'},
        goal={'files_to_compact': 'None'}
    )
    pprint('Action Plan: {}'.format(planner.action_plan))
    print('PATH: ', planner.path)
    print('Action planning: ')
    pprint(plan, indent=2)
