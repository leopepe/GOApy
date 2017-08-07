from automat import MethodicalMachine
from Goap.Sensor import Sensors
from Goap.Action import Actions
from Goap.Planner import Planner


class Automaton:
    """ A 3 State Machine Automaton: observe (aka monitor or patrol), plan and act

    """

    machine = MethodicalMachine()

    def __init__(self, name: str='Automaton', sensors: Sensors=[], actions: Actions=[]):
        self.name = name
        self.sensors = sensors
        self.actions = actions
        self.planner = Planner(actions=actions)
        self.action_plan = []
        self.action_plan_response = None
        self.sensors_responses = {}
        self.actions_response = []
        self.goal = {}

    @machine.state(initial=True)
    def observe(self):
        self.sensors_responses.update(self.sensors.run_all())

    @machine.state()
    def plan(self, initial_state: dict, final_state: dict):
        self.action_plan = self.planner.plan(initial_state, final_state)

    @machine.state()
    def act(self):
        self.actions_response = [action() for action in self.action_plan]

    @machine.input()
    def change_goal(self, goal: dict):
        self.goal = goal

    @machine.input()
    def enter_observing_state(self):
        pass

    @machine.input()
    def enter_planning_state(self):
        pass

    @machine.input()
    def enter_acting_state(self):
        pass

    @machine.output()
    def output_action_plan(self):
        return self.action_plan

    @machine.output()
    def output_actions_results(self):
        return self.action_plan_response



if __name__ == '__main__':
    pass