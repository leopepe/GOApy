from random import choice
from time import sleep
from datetime import datetime

import boto3
from Goap.StateMachine import StateMachine
from Goap.Action import Actions


class Sensors:

    def __init__(self):
        """
        :self.values: it is a shared dictionary where the sensors stores the results of its inspections
        """
        self.values = {}
        self.ec2 = boto3.client('ec2', region_name='us-west-2')
        self.rds = boto3.client('rds', region_name='us-west-2')
        self.tag = None

    def check_aws_vpc(self, tag: dict):
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        key = None
        value = None
        if len(tag) == 1:
            key, value = tag.popitem()

        if key and value:
            resp = self.ec2.describe_vpcs(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

            if len(resp['Vpcs']) == 1:
                return True
            elif len(resp['Vpcs']) > 1:
                return 'ERROR'
            elif len(resp['Vpcs']) == 0:
                return False

    def check_aws_rds(self, tag: dict):
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        key = None
        value = None
        if len(tag) == 1:
            key, value = tag.popitem()

        if key and value:
            resp = self.ec2.describe_db_instances(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

            if len(resp['DBInstances']) == 1:
                return True
            elif len(resp['DBInstances']) > 1:
                return 'ERROR'
            elif len(resp['DBInstances']) == 0:
                return False

    def check_aws_instances(self, tag: dict):
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        key = None
        value = None
        if len(tag) == 1:
            key, value = tag.popitem()

        if key and value:
            resp = self.ec2.describe_instances(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

            if len(resp['Instances']) == 1:
                return True
            elif len(resp['Instances']) > 1:
                return 'ERROR'
            elif len(resp['Instances']) == 0:
                return False

    def check_local_command_output(self, command: str=None):
        """ executes a command on the local system and expects status code 0 success.

        :param command
        :return:
        """
        # values = {}
        # self.values.update(values)
        pass

    def check_mock_module_vpc(self):
        val = choice([{'vpc': True}, {'vpc': False}])
        self.values.update(val)
        return True

    def check_mock_module_app(self):
        val = choice([{'app': True}, {'app': False}])
        self.values.update(val)
        return True

    def check_mock_module_db(self) -> bool:
        val = choice([{'db': True}, {'db': False}])
        # self.values with the result of the sensor inspections
        self.values.update(val)
        return True

    def run_all(self):
        case1 = {'vpc': False, 'db': False, 'app': False}

        case2 = {'vpc': True, 'db': True, 'app': False}

        case3 = {'vpc': True, 'db': False, 'app': False}

        case4 = {'vpc': True, 'db': 'inconsistent', 'app': True}

        case5 = {'vpc': True, 'db': True, 'app': 'unhealthy'}

        case6 = {'vpc': True, 'db': True, 'app': 'out_of_capacity'}

        cases = [case1, case2, case3, case4, case5, case6]
        case = choice(cases)
        self.values.update(case)
        return case


class Agent:
    """ Autonomous Agent Class

    """
    STD_STATES = {
        'obliterate': {'vpc': False, 'db': False, 'app': False},
        'new': {'vpc': True, 'db': True, 'app': True},
        'inconsistent': {'vpc': 'inconsistent', 'db': 'inconsistent', 'app': 'inconsistent'}
    }

    def __init__(self, name: str, actions: Actions, initial_state: dict={}, goal: dict={}):
        """

        :param name:
        :param actions:
        """
        self.name = name
        self.priorities = enumerate(
            [
                {'vpc': True, 'db': True, 'app': True},
                {'vpc': True, 'db': True, 'app': False}
            ]
        )
        # world_facts acting as a working memory, default value is []
        self.world_facts = list()
        self.world_state = initial_state
        self.sensors = Sensors()
        self.full_scan()
        # planing
        self.actions = actions
        self.goal = goal
        # self.fsm = StateMachine(states=self.actions, planner=self.planner())
        self.fsm = StateMachine(states=self.actions)

    def full_scan(self) -> dict:
        """ run all sensors and update the word_facts

        :rtype: dict
        :return: A dict containing the world facts known by the agent
        """
        self.world_state.update(self.sensors.run_all())
        return self.world_state

    def set_goal(self, goal: dict):
        """ set goal of the AA

        :param goal:
        :return:
        """
        self.goal = goal

    def run(self, goal: dict={'vpc': True, 'db': True, 'app': True}):
        """ start the AA

        :return:
        """
        self.set_goal(goal)
        while True:
            # update all sensors
            self.full_scan()
            print('\n\n\n###\n###\n###')
            print('[INFO] Starting {}'.format(datetime.now()))
            print('[INFO] Goal: {}'.format(self.goal))
            print('[INFO] Current World State: {}'.format(self.world_state))

            if self.world_state != self.goal:
                actions_result = self.fsm.start(init_state=self.world_state, end_state=self.goal)
                if not actions_result:
                    print('[ERROR]: Unknown state\n[ERROR]: Nothing to be done, need manual interaction\n{}')
                    self.world_state = self.STD_STATES['inconsistent']
                    actions_result = self.fsm.start(init_state=self.world_state, end_state=self.STD_STATES['obliterate'])

                print('[INFO] Plan executed: {}'.format(actions_result))

            print('Sleeping 7 sec from {}'.format(datetime.now()))
            sleep(7)


if __name__ == '__main__':
    from Goap.Action import Actions
    # import pprint

    # ACTIONS
    actions = Actions()
    # VPC/Network set
    actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    actions.add_action(
        name='DestroyVPC',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': False, 'db': False, 'app': False}
    )
    # DB set
    actions.add_action(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    actions.add_action(
        name='DestroyDB',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # APP set
    actions.add_action(
        name='CreateApp',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': True, 'app': True}
    )
    actions.add_action(
        name='StopApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'unhealthy'},
        effects={'vpc': True, 'db': True, 'app': 'stopped'}
    )
    actions.add_action(
        name='TerminateStoppedApps',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    # inconsistent app
    actions.add_action(
        name='DestroyInconsistentApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'inconsistent'},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    actions.add_action(
        name='RecreateInconsistentDb',
        pre_conditions={'vpc': True, 'db': 'inconsistent', 'app': True},
        effects={'vpc': True, 'db': True, 'app': 'stopped'}
    )
    # out of capacity
    actions.add_action(
        name='IncreaseAppCapacity',
        pre_conditions={'vpc': True, 'db': True, 'app': 'out_of_capacity'},
        effects={'vpc': True, 'db': True, 'app': True}
    )
    actions.add_action(
        name='TerminateStoppedApps',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    init_state = {'vpc': False, 'app': False, 'db': False}
    init_goal = {'vpc': True, 'db': True, 'app': True}
    ai_cloud_builder = Agent(name='CloudBuilder', actions=actions)
    ai_cloud_builder.run()
