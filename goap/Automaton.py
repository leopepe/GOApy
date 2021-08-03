from datetime import datetime
from automat import MethodicalMachine
from goap.Sensor import Sensors
from goap.Action import Actions
from goap.Planner import Planner
from goap.WorldState import WorldState
from time import sleep


class Fact(object):
    def __init__(self, sensor, data, binding):
        self.binding = binding
        self.data = data
        self.time_stamp = datetime.now()
        self.parent_sensor = sensor

    def __str__(self):
        return "{}: {}".format(self.binding, self.data)

    def __repr__(self):
        return self.__str__()


class AutomatonPriorities:
    def __init__(self, items: list):
        self._items = items

    def __iter__(self):
        return self._items

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return self.__repr__()


class Automaton:
    """ A 3 State Machine Automaton: observing (aka monitor or patrol), planning and acting """

    machine = MethodicalMachine()

    def __init__(
            self,
            name: str,
            sensors: Sensors,
            actions: Actions,
            world_state_facts: dict):
        # setup
        self.world_state = WorldState(world_state_facts)
        self.working_memory = []
        self.name = name
        self.sensors = sensors
        self.actions = actions
        self.planner = Planner(actions=actions)
        #
        self.action_plan = []
        self.action_plan_response = None
        self.sensors_responses = {}
        self.actions_response = []
        self.goal = {}

    def __sense_environment(self):
        for sensor in self.sensors:
            self.working_memory.append(
                Fact(
                    sensor=sensor.name,
                    data=sensor.exec(),
                    binding=sensor.binding
                )
            )
        for fact in self.working_memory:
            setattr(
                self.world_state,
                fact.binding,
                fact.data.response
            )

    def __set_action_plan(self):
        self.action_plan = self.planner.plan(self.world_state, self.goal)
        return self.action_plan

    def __execute_action_plan(self):
        self.actions_response = [action[2]['object'].exec()
                                 for action in self.action_plan]
        return 'Action planning execution results: {}'.format(
            self.action_plan_response)

    @machine.state(initial=True)
    def waiting_orders(self):
        """ Waiting goal / orders """

    @machine.state()
    def sensing(self):
        """ Running sensors and assimilating sensor's responses """

    @machine.state()
    def planning(self):
        """ Generating action plan to change actual world state to achieve goal """

    @machine.state()
    def acting(self):
        """ Executing action plan"""

    @machine.input()
    def wait(self):
        """ Input waiting_orders state """

    @machine.input()
    def sense(self):
        """ Input sense state """

    @machine.output()
    def __sense(self):
        """ Execute sensors """
        self.__sense_environment()

    @machine.input()
    def plan(self):
        """ Input for planning state """

    @machine.output()
    def __plan(self):
        """ Generate action plan """
        self.__set_action_plan()

    @machine.input()
    def act(self):
        """ Input for acting state"""

    @machine.output()
    def __act(self):
        """ Execute action plan """
        self.__execute_action_plan()

    @machine.input()
    def input_goal(self, goal):
        """ Change / Set AI goal """

    @machine.output()
    def __input_goal(self, goal):
        """ Actually sets goal """
        self.goal = goal

    @machine.output()
    def __reset_working_memory(self):
        self.working_memory = []

    # cyclical main states
    waiting_orders.upon(sense, enter=sensing, outputs=[__sense])
    sensing.upon(plan, enter=planning, outputs=[__plan])
    planning.upon(act, enter=acting, outputs=[__act])
    acting.upon(
        sense,
        enter=sensing,
        outputs=[
            __reset_working_memory,
            __sense])
    # change orders
    waiting_orders.upon(
        input_goal,
        enter=waiting_orders,
        outputs=[__input_goal])
    planning.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    acting.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    # reset working memory from sensing
    sensing.upon(wait, enter=waiting_orders, outputs=[__reset_working_memory])


class AutomatonController(object):

    def __init__(
            self,
            actions: Actions,
            sensors: Sensors,
            name: str,
            world_state: dict):
        self.automaton = Automaton(
            actions=actions,
            sensors=sensors,
            name=name,
            world_state_facts=world_state)

    @property
    def world_state(self):
        return self.automaton.world_state

    @world_state.setter
    def world_state(self, value):
        self.automaton.world_state = value

    @property
    def goal(self):
        return self.automaton.goal

    @goal.setter
    def goal(self, value):
        self.automaton.input_goal(value)

    def start(self):
        while True:
            self.automaton.sense()
            if self.automaton.world_state != self.goal:
                print(
                    'World state differs from goal: \nState: {}\nGoal: {}'.format(
                        self.automaton.world_state, self.goal))
                print('Need to find an action plan')
                self.automaton.plan()
                print(
                    'Plain found. Will execute the action plan: {}'.format(
                        self.automaton.action_plan))
                self.automaton.act()
            else:
                print("World state equals to goal: {}".format(self.goal))
                self.automaton.wait()
            sleep(5)
