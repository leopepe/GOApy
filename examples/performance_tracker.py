from goap.action import Actions
from goap.agent import Agent


class PerformanceTracker:

    PRIORITIES = (
        1, {'vpc': True, 'db': True, 'app': True},
        2, {'vpc': 'monitoring', 'db': 'monitoring', 'app': 'monitoring'},
    )

    def __init__(self):
        # ACTIONS
        actions = Actions()
        # increase app capacity
        actions.add_action(
            name='IncreaseAppCapacity',
            pre_conditions={'vpc': True, 'db': True, 'app': 'out_of_capacity'},
            effects={'vpc': True, 'db': True, 'app': True}
        )
        # increase db capacity
        actions.add_action(
            name='IncreaseAppCapacity',
            pre_conditions={'vpc': True, 'db': 'out_of_capacity', 'app': True},
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
