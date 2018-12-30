import unittest
from goap.action import Actions
from goap.Sensor import Sensors
from goap.Automaton import Automaton


class AutomatonTest(unittest.TestCase):

    def setUp(self):
        self.actions = Actions()
        self.sensors = Sensors()
        self.automaton = Automaton()

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
        ai = Automaton(name='infra_builder', actions=aws_actions, sensors=aws_sensors, world_state=world_state_matrix)
        # Control
        # what is the environment status? what does the sensors return? ai has a goal?
        # goal = priorities # object not working returning object rather then dict
        ai.input_goal(goal)
        ai.sense()
        pp.pprint(
            'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(ai.world_state, ai.action_plan,
                                                                        ai.actions_response)
        )
        ai.plan()
        ai.act()
        pp.pprint(
            'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(ai.world_state, ai.action_plan,
                                                                        ai.actions_response)
        )