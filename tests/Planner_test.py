from os import path
import unittest
import subprocess
from pprint import PrettyPrinter

import networkx as nx

from Goap.WorldState import WorldState
from Goap.Action import Actions
from Goap.Planner import Planner


class PlannerTest(unittest.TestCase):

    @staticmethod
    def __reset_environment():
        if path.isdir('/tmp/goap_tmp'):
            subprocess.call(['rm', '-rf', '/tmp/goap_tmp'])

    def __print(self):
        self.print.pprint(
            'Nodes: {}, Edges: {}'.format(self.planner.graph.nodes, self.planner.graph.edges)
        )

    def setUp(self):
        self.print = PrettyPrinter(indent=4)
        self.setUpDirHandlerCMD()
        self.setUpLvmCMD()
        self.init_ws = WorldState({"tmp_dir_state": False, "tmp_dir_content": False, })
        self.gs = WorldState({"tmp_dir_state": True, "tmp_dir_content": True, })
        self.planner = Planner(actions=self.dir_handler_cmd)

    def setUpDirHandlerCMD(self):
        self.dir_handler_cmd = Actions()
        self.dir_handler_cmd.add(
            name='CreateTmpDir',
            pre_conditions={'tmp_dir_state': False, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': False},
            shell='mkdir -p /tmp/goap_tmp'
        )
        self.dir_handler_cmd.add(
            name='CreateToken',
            pre_conditions={'tmp_dir_state': True, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': True},
            shell='touch /tmp/goap_tmp/.token'
        )

    def setUpLvmCMD(self):
        self.lv_act = Actions()
        self.lv_act.add(
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
        self.lv_act.add(
            name='ExpandVG',
            pre_conditions={
                'vg_need_expansion': True,
                'pv_need_expansion': False,
            },
            effects={
                'vg_need_expansion': False,
            },
            shell='echo expand_vg'
        )
        self.lv_act.add(
            name='ExpandPV',
            pre_conditions={
                'pv_need_expansion': True,
            },
            effects={
                'pv_need_expansion': False,
            },
            shell='echo purge_old_files',
            cost=1.5,
        )

    def test_set_goal(self):
        self.planner.goal = self.gs
        assert self.gs == self.planner.goal

    def test_graph_isomorphic(self):
        from Goap.Planner import Node
        from Goap.Planner import Edge

        acts = Actions()
        acts.add(
            name='CreateTmpDir',
            pre_conditions={'tmp_dir_state': False, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': False},
            shell='mkdir -p /tmp/goap_tmp'
        )
        acts.add(
            name='CreateToken',
            pre_conditions={'tmp_dir_state': True, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': True},
            shell='touch /tmp/goap_tmp/.token'
        )
        node1 = Node(attributes={'tmp_dir_state': False, 'tmp_dir_content': False})
        node2 = Node(attributes={'tmp_dir_state': True, 'tmp_dir_content': False})
        node3 = Node(attributes={'tmp_dir_state': True, 'tmp_dir_content': True})
        edge1 = Edge(name='CreateTmpDir', predecessor=node1, successor=node2, obj=acts.get('CreateTmpDir'))
        edge2 = Edge(name='CreateToken', predecessor=node2, successor=node3, obj=acts.get('CreateToken'))
        g1 = nx.DiGraph(nodes=[node1, node2, node3], edges=[edge1, edge2])
        g2 = self.planner.graph.directed
        assert nx.is_isomorphic(g1, g2) is True

    def test_plan(self):
        create_tmp_dir = self.planner.actions.get('CreateTmpDir')
        create_token = self.planner.actions.get('CreateToken')
        plan = self.planner.plan(state=self.init_ws, goal=self.gs)
        action_plan = [action[2]['object'] for action in plan]
        assert action_plan == [create_tmp_dir, create_token]

