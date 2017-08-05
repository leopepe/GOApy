from automat import MethodicalMachine
from Goap.Sensor import Sensors
from Goap.Action import Actions
from Goap.Planner import Planner


class Automaton:

    machine = MethodicalMachine()

    def __init__(self, name: str='Automaton', sensors: Sensors=[], actions: Actions=[]):
        self.name = name
        self.sensors = sensors
        self.actions = actions
        self.planner = Planner(actions=actions)
        self.action_plan = []
        self.action_plan_response = None

    @machine.state(initial=True)
    def observe(self):
        self.sensors.run_all()

    @machine.state()
    def plan(self):
        self.planning.plan()

    @machine.state()
    def act(self):
        self.action_plan_response = [action() for action in self.actions]

    @machine.input()
    def change_goal(self, goal: dict):
        pass

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

    enter_observing_state.upon()

if __name__ == '__main__':
    pass