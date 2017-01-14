from Goap.Action import Actions
from Goap.StateMachine import StateMachine
from random import choice
from time import sleep
from datetime import datetime


class Sensors:

    def __init__(self):
        self.values = {}

    def check_aws_resource(self):
        pass

    def check_terraform_module(self):
        pass

    def check_module_vpc(self):
        val = choice([{'vpc': True}, {'vpc': False}])
        self.values.update(val)
        return True

    def check_module_app(self):
        val = choice([{'app': True}, {'app': False}])
        self.values.update(val)
        return True

    def check_module_db(self) -> bool:
        val = choice([{'db': True}, {'db': False}])
        self.values.update(val)
        return True

    def run_all(self):
        self.check_module_vpc()
        self.check_module_db()
        self.check_module_app()
        return self.values


class Agent:
    """ Autonomous Agent Class

    """

    def __init__(self, name: str, actions: Actions, init_state: dict={}, goal: dict={}) -> object:
        """

        :param name:
        :param actions:
        """
        self.name = name
        # world_facts act as a working memory, default value is {}
        self.world_facts = init_state
        self.sensors = Sensors()
        self.full_scan()
        # planing
        self.actions = actions
        # self.planner = Planner(actions)
        self.goal = goal
        # self.fsm = StateMachine(states=self.actions, planner=self.planner())
        self.fsm = StateMachine(states=self.actions)

    def full_scan(self):
        """ run all sensors and update the word_facts

        :return:
        """
        self.world_facts = self.sensors.run_all()
        return self.world_facts

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
        prev_state = self.world_facts
        change_detected = False
        while True:
            # update all sensors
            self.full_scan()
            print('\n\n\n###\n###\n###')
            print('Starting {}'.format(datetime.now()))
            print('Goal: {}'.format(self.goal))
            print('Current World State: {}'.format(self.world_facts))
            print('###\n###')

            # Alert for changes on the environment
            if self.world_facts != prev_state:
                change_detected = True
                print('[WARN] Change identified by sensor...')

            if self.world_facts != self.goal:
                print('[INFO] Planning...')
                self.fsm.set_transitions(init_state=self.world_facts, end_state=self.goal)
                print('[INFO] Plan: {}'.format(self.fsm.get_transitions()))
                self.fsm.start()

            print('Sleeping 7 sec from {}'.format(datetime.now()))
            sleep(7)


if __name__ == '__main__':
    from Goap.Action import Actions
    import pprint

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
    init_state = {'vpc': False, 'app': False, 'db': False}
    init_goal = {'vpc': True, 'db': True, 'app': True}
    ai_cloud_builder = Agent(name='CloudBuilder', actions=actions)
    ai_cloud_builder.run()
