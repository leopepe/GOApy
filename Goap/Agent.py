from Goap.Planner import Planner
"""
  DONE
    - Plan actually works now!
    - Impl. Action
    - Impl. Planner
  TODO
    - FSM

"""


class Agent:
    """
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
    ai_cloud_builder = Agent(name='CloudBuilder', state=init_state, goal=init_goal, actions=actions)
    result = ai_cloud_builder.start()
    pprint.pprint(result, indent=2, width=80)

    """

    def __init__(self, name: str, state: dict, goal: dict, actions: object) -> object:
        self.name = name
        self.state = state
        self.goal = goal
        self.actions = actions
        self.planner = Planner(self.actions, self.state, self.goal)

    def __update(self):
        """
            updates state and goal

        :return:
        """
        new_goal = None
        new_state = None
        self.goal = new_goal
        self.state = new_state

    def get_plan(self):
        """

        :return:
        """
        return self.planner.plan(self.state, self.goal)

    def start(self):
        """

        :return: tuple with action.name and result of action execution (action.name, action.do)
        """
        response = []
        [response.append(action[2]['object'].do) for action in self.get_plan()]
        return response

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
    ai_cloud_builder = Agent(name='CloudBuilder', state=init_state, goal=init_goal, actions=actions)
    result = ai_cloud_builder.start()
    pprint.pprint(result, indent=2, width=80)
