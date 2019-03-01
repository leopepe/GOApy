from os import path
import unittest
import subprocess
from pprint import PrettyPrinter
from Goap.WorldState import WorldState
from Goap.Action import Actions
from Goap.Planner2 import Planner


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
        self.init_ws = WorldState({"tmp_dir_state": False, "tmp_dir_content": False, })
        self.gs = WorldState({"tmp_dir_state": True, "tmp_dir_content": True, })
        self.actions = Actions()
        self.actions.add(
            name='CreateTmpDir',
            pre_conditions={'tmp_dir_state': False, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': False},
            shell='mkdir -p /tmp/goap_tmp'
        )
        self.actions.add(
            name='CreateToken',
            pre_conditions={'tmp_dir_state': True, 'tmp_dir_content': False},
            effects={'tmp_dir_state': True, 'tmp_dir_content': True},
            shell='touch /tmp/goap_tmp/.token'
        )
        self.planner = Planner(world_state=self.init_ws, actions=self.actions)

    def setLvmCmd(self):
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
            },
            effects={
                'vg_need_expansion': False,
            },
            shell='echo expand_vg'
        )
        self.lv_act.add(
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

    def test_set_goal(self):
        self.planner.goal = self.gs
        assert self.gs == self.planner.goal

    def test_nodes(self):
        assert self.planner.graph.nodes == [
            (0, {'tmp_dir_state': 'not_exist', 'tmp_dir_content': 'token_not_found'}),
            (1, {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'}),
            (2, {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_found'})
        ]

    def test_edges(self):
        assert self.planner.graph.edges == [
            (0, 1, {'object': self.actions.get('CreateTmpDir')}),
            (1, 2, {'object': self.actions.get('CreateToken')})
        ]

    def test_planning(self):
        self.planner.plan(state=self.init_ws, goal=self.gs)
        assert self.planner.action_plan == [
            (0, 1, {'object': self.actions.get('CreateTmpDir')}),
            (1, 2, {'object': self.actions.get('CreateToken')})
        ]

    def test_all_possible_states(self):
        assert self.planner.actions.states() == [
            {'tmp_dir_state': 'not_exist', 'tmp_dir_content': 'token_not_found'},
            {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'},
            {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_found'}
        ]


