from GOAP.Planner import Planner
"""
    implements: Action, Planner, FSM
"""


class Agent:
    """
        from GOAP.Action import Actions
        import pprint
        actions = Actions()
        actions.add_action(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'app': False, 'db': False},
            effects={'vpc': True, 'app': False, 'db': False}
        )
        actions.add_action(
            name='CreateDB',
            pre_conditions={'vpc': True, 'app': False, 'db': False},
            effects={'vpc': True, 'app': False, 'db': True}
        )
        actions.add_action(
            name='CreateApp',
            pre_conditions={'vpc': True, 'app': False, 'db': True},
            effects={'vpc': True, 'app': True, 'db': True}
        )
        init_state = {'vpc': False, 'app': False, 'db': False}
        init_goal = {'vpc': True, 'db': True, 'app': True}
        builder = Agent(name='CloudBuilder', state=init_state, goal=init_goal, actions=actions)
        result = builder.actuate()
        pprint.pprint(result, indent=2)

        [ ( 'CreateVPC',
        <bound method Action.do of {'CreateVPC': {'pre_conditions': {'app': False, 'db': False, 'vpc': False}, 'effects': {'app': False, 'db': False, 'vpc': True}} }>),
        ( 'CreateDB',
        <bound method Action.do of {'CreateDB': {'pre_conditions': {'app': False, 'db': False, 'vpc': True}, 'effects': {'app': False, 'db': True, 'vpc': True}} }>),
        ( 'CreateApp',
        <bound method Action.do of {'CreateApp': {'pre_conditions': {'app': False, 'db': True, 'vpc': True}, 'effects': {'app': True, 'db': True, 'vpc': True}} }>)]
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
        return self.planner.plan()

    def actuate(self):
        """

        :return: tuple with action.name and result of action execution (action.name, action.do)
        """
        result = [(action.name, action.do) for action in self.get_plan()]
        return result

if __name__ == '__main__':
    from GOAP.Action import Actions
    import pprint
    actions = Actions()
    actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'app': False, 'db': False},
        effects={'vpc': True, 'app': False, 'db': False}
    )
    actions.add_action(
        name='CreateDB',
        pre_conditions={'vpc': True, 'app': False, 'db': False},
        effects={'vpc': True, 'app': False, 'db': True}
    )
    actions.add_action(
        name='CreateApp',
        pre_conditions={'vpc': True, 'app': False, 'db': True},
        effects={'vpc': True, 'app': True, 'db': True}
    )
    init_state = {'vpc': False, 'app': False, 'db': False}
    init_goal = {'vpc': True, 'db': True, 'app': True}
    builder = Agent(name='CloudBuilder', state=init_state, goal=init_goal, actions=actions)
    result = builder.actuate()
    pprint.pprint(result, indent=2, width=80)
