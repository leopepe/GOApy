from GOAP import Planner
"""
    implements: Action, Planner, FSM
"""


class State:

    def __init__(self, name, facts: dict):
        self.name = name
        self.facts = facts

    def add_fact(self, **kwargs):
        self.facts.update(kwargs)

    def remove_fact(self, **kwargs):
        self.facts.__delitem__(kwargs)

    def __str__(self):
        return 'State: {0}, Facts: {1}'.format(self.name, self.facts)

    def __repr__(self):
        return self.__str__()


class States:

    def __init__(self):
        self.states = list

    def __str__(self):
        return '{}'.format(self.states)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.states)


class Agent:

    def __init__(self, name: str, state: State, goal: str, actions: list):
        self.name = name
        self.state = state
        self.goal = goal
        self.actions = actions
        # self.plan = Planner()

    def inspect_world(self):
        pass

    def update_state(self):
        pass

    def execute_plan(self):
        pass

