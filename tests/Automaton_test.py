import unittest

from goap.action import Actions
from goap.automaton import Automaton
from goap.sensor import Sensors


class AutomatonTest(unittest.TestCase):

    def setUp(self):
        self.actions = Actions()
        self.sensors = Sensors()
        self.automaton = None

    def test_all(self):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(indent=4)
        world_state_matrix = {
            "tmp_dir_state": 'Unknown',
            "print_content": 'Unknown',
        }
        goal = {
            "tmp_dir_state": "available",
            "db_state": "available",
        }
        self.actions.add(
            name='ListTmpDir',
            pre_conditions={'tmp_dir_state': 'exist', 'print_content': 'not_exist'},
            effects={'tmp_dir_state': 'exist', 'print_content': 'printed'},
            shell='ls -ltr "/tmp/goap_tmp"'
        )
        self.actions.add(
            name='CreateTmpDir',
            pre_conditions={'tmp_dir_state': 'exist', 'print_content': 'not_exist'},
            effects={'tmp_dir_state': 'exist', 'print_content': 'printed'},
            shell='ls -ltr "/tmp/goap_tmp"'
        )
        self.sensors.add(
            name='SenseTmpDirState',
            shell='ls -ltrd /tmp/goap_tmp',
            binding='tmp_dir_state'
        )

        self.ai = Automaton(name='infra_builder', actions=self.actions, sensors=self.sensors,
                            world_state=world_state_matrix)
        # Control
        # what is the environment status? what does the sensors return? ai has a goal?
        # goal = priorities # object not working returning object rather then dict
        self.ai.input_goal(goal)
        self.ai.sense()
        pp.pprint(
            'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(self.ai.world_state, self.ai.action_plan,
                                                                        self.ai.actions_response)
        )
        self.ai.plan()
        self.ai.act()
        pp.pprint(
            'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(self.ai.world_state, self.ai.action_plan,
                                                                        self.ai.actions_response)
        )
