from goap.action import Actions
from goap.Agent import Agent


class CloudBuild:

    PRIORITIES = [
        {'vpc': True, 'db': True, 'app': True},
        {'vpc': 'monitoring', 'db': 'monitoring', 'app': 'monitoring'},
    ]

    def __init__(self):
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
        # init_state = {'vpc': False, 'app': False, 'db': False}
        init_goal = {'vpc': True, 'db': True, 'app': True}
        self.ai = Agent(name='CloudBuilder', actions=self.actions, goal=init_goal)

    def run_agent(self):
        self.ai.run()


if __name__ == '__main__':
    ai = CloudBuild()
    ai.run_agent()
