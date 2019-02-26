from os import path
import unittest
import subprocess
from pprint import PrettyPrinter
from Goap.Action import Actions
from Goap.Automaton import Planner


class PlannerTest(unittest.TestCase):

    @staticmethod
    def __reset_environment():
        if path.isdir('/tmp/goap_tmp'):
            subprocess.call(['rm', '-rf', '/tmp/goap_tmp'])

    def __print(self):
        self.print.pprint(
            'Nodes: {}, Edges: {}'.format(self.planner.nodes, self.planner.edges)
        )

    def setUp(self):
        self.print = PrettyPrinter(indent=4)
        self.world_state_matrix = {
            "tmp_dir_state": 'not_exist',
            "tmp_dir_content": 'token_not_found',
        }
        self.goal = {
            "tmp_dir_state": "exist",
            "tmp_dir_content": "token_found",
        }
        self.actions = Actions()
        self.actions.add(
            name='CreateTmpDir',
            pre_conditions={'tmp_dir_state': 'not_exist', 'tmp_dir_content': 'token_not_found'},
            effects={'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'},
            shell='mkdir -p /tmp/goap_tmp'
        )
        self.actions.add(
            name='CreateToken',
            pre_conditions={'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'},
            effects={'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_found'},
            shell='touch /tmp/goap_tmp/.token'
        )
        self.planner = Planner(actions=self.actions)

    def test_set_goal(self):
        self.planner.goal = self.goal
        assert self.goal == self.planner.goal

    def test_nodes(self):
        assert self.planner.nodes == [
            (0, {'tmp_dir_state': 'not_exist', 'tmp_dir_content': 'token_not_found'}),
            (1, {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'}),
            (2, {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_found'})
        ]

    def test_edges(self):
        assert self.planner.edges == [
            (0, 1, {'object': self.actions.get('CreateTmpDir')}),
            (1, 2, {'object': self.actions.get('CreateToken')})
        ]

    def test_planning(self):
        self.planner.plan(init_state=self.world_state_matrix, goal=self.goal)
        assert self.planner.action_plan == [
            (0, 1, {'object': self.actions.get('CreateTmpDir')}),
            (1, 2, {'object': self.actions.get('CreateToken')})
        ]

    def test_all_possible_states(self):
        assert self.planner.actions.actions_attributes() == [
            {'tmp_dir_state': 'not_exist', 'tmp_dir_content': 'token_not_found'},
            {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'},
            {'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_found'}
        ]


