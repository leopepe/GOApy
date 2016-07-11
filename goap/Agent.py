from World import Actions
from World import Action
from Planner import Planner


class Agent(Actions):

    def __init__(self):
        self.name = None
        self.goal = None
        self.planner = Planner()

    def inspect(self):
        pass

    def act(self, action: Action):
        pass

