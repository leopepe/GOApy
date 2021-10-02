from goap.utils.os.shell_command import ShellCommand
from os import path
import unittest
import subprocess
from pprint import PrettyPrinter

import networkx as nx

from goap.WorldState import WorldState
from goap.Action import Actions
from goap.Planner import Planner


class PlannerTest(unittest.TestCase):

    @staticmethod
    def __reset_environment():
        if path.isdir('/tmp/goap_tmp'):
            subprocess.call(['rm', '-rf', '/tmp/goap_tmp'])

    def __print(self):
        self.print.pprint(
            'Nodes: {}, Edges: {}'.format(
                self.planner.graph.nodes,
                self.planner.graph.edges))

    def setUp(self):
        # init actions
        self.dir_handler_cmd = Actions()
        self.lv_act = Actions()
        # setup actions
        self.mkdir = ShellCommand(command='mkdir -p /tmp/goap_tmp')
        self.mktoken = ShellCommand(command='touch /tmp/goap_tmp/.token')
        self.mkecho = ShellCommand(command='echo mocked')
        # self.setUpLvmCMD()
        # self.setUpDirHandlerCMD()
        # init planner
        self.print = PrettyPrinter(indent=4)
        self.init_ws = WorldState(
            {"tmp_dir_state": False, "tmp_dir_content": False, })
        self.gs = WorldState(
            {"tmp_dir_state": True, "tmp_dir_content": True, })
        self.planner = Planner(actions=self.dir_handler_cmd)

    def tearDown(self) -> None:
        self.dir_handler_cmd = []
        self.lv_act = []
        self.init_ws = None
        self.gs = {}
        self.planner = None

    def setUpDirHandlerCMD(self):
        self.dir_handler_cmd.add(
            name='CreateTmpDir',
            conditions={'tmp_dir_state': False, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': False},
            func=self.mkdir
        )
        self.dir_handler_cmd.add(
            name='CreateToken',
            conditions={'tmp_dir_state': True, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': True},
            func=self.mktoken
        )

    def setUpLvmCMD(self):
        self.lv_act.add(
            name='ExpandLV',
            conditions={
                'lv_need_expansion': True,
                'vg_need_expansion': False,
            },
            effects={
                'lv_need_expansion': False,
            },
            func=self.mkecho,
            cost=1.0
        )
        self.lv_act.add(
            name='ExpandVG',
            conditions={
                'vg_need_expansion': True,
                'pv_need_expansion': False,
            },
            effects={
                'vg_need_expansion': False,
            },
            func=self.mkecho,
        )
        self.lv_act.add(
            name='ExpandPV',
            conditions={
                'pv_need_expansion': True,
            },
            effects={
                'pv_need_expansion': False,
            },
            func=self.mkecho,
            cost=1.5,
        )

    def test_set_goal(self):
        self.planner.goal = self.gs
        assert self.gs == self.planner.goal

    def test_graph_isomorphic(self):
        from goap.Planner import Node
        from goap.Planner import Edge

        acts = Actions()
        acts.add(
            name='CreateTmpDirIso',
            conditions={'tmp_dir_state': False, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': False},
            func=self.mkdir
        )
        acts.add(
            name='CreateTokenIso',
            conditions={'tmp_dir_state': True, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': True},
            func=self.mktoken
        )
        node1 = Node(
            attributes={
                'tmp_dir_state': False,
                'tmp_dir_content': False})
        node2 = Node(
            attributes={
                'tmp_dir_state': True,
                'tmp_dir_content': False})
        node3 = Node(
            attributes={
                'tmp_dir_state': True,
                'tmp_dir_content': True})
        edge1 = Edge(
            name='CreateTmpDirIso',
            predecessor=node1,
            successor=node2,
            obj=acts.get('CreateTmpDirIso'))
        edge2 = Edge(
            name='CreateTokenIso',
            predecessor=node2,
            successor=node3,
            obj=acts.get('CreateTokenIso'))
        g1 = nx.DiGraph(nodes=[node1, node2, node3], edges=[edge1, edge2])
        g2 = self.planner.graph.directed
        assert nx.is_isomorphic(g1, g2) is True

    def test_plan(self):
        self.setUpDirHandlerCMD()
        create_tmp_dir = self.planner.actions.get('CreateTmpDir')
        create_token = self.planner.actions.get('CreateToken')
        plan = self.planner.plan(state=self.init_ws, goal=self.gs)
        print(type(plan))
        print(plan)
        action_plan = [action[2]['object'] for action in plan]
        print(action_plan)
        assert action_plan == [create_tmp_dir, create_token]
