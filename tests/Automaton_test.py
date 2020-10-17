import subprocess
import unittest
from os import path
from pprint import PrettyPrinter

from Goap.Action import Action, Actions
from Goap.Automaton import Automaton
from Goap.Sensor import Sensor, Sensors
from Goap.utils.os.ShellCommand import ShellCommand


ENV_DIR = '/tmp/goap_tmp'


class AutomatonTest(unittest.TestCase):

    @staticmethod
    def __reset_environment():
        if path.isdir('/tmp/goap_tmp'):
            subprocess.check_output(['rm', '-rf', ENV_DIR], timeout=5)

    def __print(self):
        self.print.pprint(
            'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(
                self.automaton.world_state,
                self.automaton.action_plan,
                self.automaton.actions_response))

    def setupSensors(self):
        self.sense_dir_state = Sensor(
            name='SenseDirState',
            func=ShellCommand(
                command='if [ -d "/tmp/goap_tmp" ]; then printf "exist"; else printf "not_exist"; fi'),
            binding='tmp_dir_state'
        )
        self.sense_dir_content = Sensor(
            name='SenseTmpDirContent',
            func=ShellCommand(
                command='[ -f /tmp/goap_tmp/.token ] && printf "token_found" || printf "token_not_found"'),
            binding='tmp_dir_content'
        )

    def setupActions(self):
        self.create_dir = Action(
            name='CreateDir',
            pre_conditions={
                'tmp_dir_state': 'not_exist',
                'tmp_dir_content': 'token_not_found'},
            effects={
                'tmp_dir_state': 'exist',
                'tmp_dir_content': 'token_not_found'},
            func=ShellCommand(command='mkdir -p /tmp/goap_tmp')
        )
        self.create_file_token = Action(
            name='CreateFileToken',
            pre_conditions={
                'tmp_dir_state': 'exist',
                'tmp_dir_content': 'token_not_found'},
            effects={
                'tmp_dir_state': 'exist',
                'tmp_dir_content': 'token_found'},
            func=ShellCommand(command='touch /tmp/goap_tmp/.token')
        )

    def setUp(self):
        self.print = PrettyPrinter(indent=4)

        self.goal = {
            "tmp_dir_state": "exist",
            "tmp_dir_content": "token_found",
        }
        self.setupActions()
        self.setupSensors()
        self.actions = Actions(actions=[self.create_dir, self.create_file_token])
        self.sensors = Sensors(sensors=[self.sense_dir_state, self.sense_dir_content])

        world_state_matrix = {
            "tmp_dir_state": 'Unknown',
            "tmp_dir_content": 'Unknown',
        }
        self.automaton = Automaton(
            name='directory_watcher',
            actions=self.actions,
            sensors=self.sensors,
            world_state=world_state_matrix
        )

    def test_sensing(self):
        self.__reset_environment()
        # self.setupSensors()
        self.automaton.input_goal(self.goal)
        self.automaton.sense()
        assert self.automaton.world_state == {
            'tmp_dir_state': 'not_exist',
            'tmp_dir_content': 'token_not_found'}

    def test_planning(self):
        create_tmp_dir = self.actions.get('CreateDir')
        create_token = self.actions.get('CreateFileToken')
        self.__reset_environment()
        self.automaton.input_goal(self.goal)
        self.automaton.sense()
        self.automaton.plan()
        action_plan = [action[2]['object']
                       for action in self.automaton.action_plan]
        assert action_plan == [create_tmp_dir, create_token]

    def test_acting(self):
        self.__reset_environment()
        # self.setupActions()
        self.automaton.input_goal(self.goal)
        self.automaton.sense()
        self.automaton.plan()
        self.automaton.act()
        assert path.isdir(
            '/tmp/goap_tmp') and path.isfile('/tmp/goap_tmp/.token')
