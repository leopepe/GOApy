from goap.action import Actions
from goap.Agent import Agent


class DeploymentAgent:

    PRIORITIES = [
        {'vpc': True, 'db': True, 'app': True},
        {'vpc': 'monitoring', 'db': 'monitoring', 'app': 'monitoring'},
    ]

    def __init__(self):
        # ACTIONS
        self.actions = Actions()
        # update app
        self.actions.add_action(
            name='UpdateApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'version_out_of_date'},
            effects={'vpc': True, 'db': True, 'app': True}
        )
        # rollback change
        self.actions.add_action(
            name='RollbackApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'need_rollback'},
            effects={'vpc': True, 'db': True, 'app': True}
        )
        # init_state = {'vpc': False, 'app': False, 'db': False}
        init_goal = {'vpc': True, 'db': True, 'app': True}
        self.ai = Agent(name='CloudBuilder', actions=self.actions, goal=init_goal)

    def run_agent(self):
        self.ai.run()


if __name__ == '__main__':
    ai = PerformanceTracker()
    ai.run_agent()


