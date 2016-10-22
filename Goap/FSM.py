class State:

    def __init__(self, name):
        self.name = name


class StateMachine:

    def __init__(self):
        self.states = {}
        self.initial_state = None

    def add_state(self, name: str, state: str=None):
        pass

    def transition(self):
        pass

    def exec_state(self, cargo):
        pass

