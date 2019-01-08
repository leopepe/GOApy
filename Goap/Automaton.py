from datetime import datetime
from automat import MethodicalMachine
from Goap.Sensor import Sensors
from Goap.Action import Actions
from Goap.Planner import Planner
from rx import Observable
from time import sleep


class Fact(object):
    def __init__(self, sensor, data, binding):
        self.binding = binding
        self.data = data
        self.time_stamp = datetime.now()
        self.parent_sensor = sensor

    def __str__(self):
        return '{}: {}'.format(self.binding, self.data)

    def __repr__(self):
        return self.__str__()


class WorldState(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(WorldState, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(WorldState, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(WorldState, self).__delitem__(key)
        del self.__dict__[key]


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

    def __init__(self, name: str, sensors: Sensors, actions: Actions, world_state: dict):
        # setup
        self.world_state = WorldState(world_state)
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
        Observable.from_(self.sensors). \
            subscribe(
            lambda sensor: self.working_memory.append(Fact(sensor=sensor.name, data=sensor.exec(), binding=sensor.binding))
        )
        Observable.from_(self.working_memory). \
            subscribe(
            lambda fact: setattr(self.world_state, fact.binding, fact.data.response)
        )

    def __set_action_plan(self):
        self.action_plan = self.planner.plan(self.world_state, self.goal)
        return self.action_plan

    def __execute_action_plan(self):
        # [print(action[2]['object']) for action in self.action_plan]
        self.actions_response = [self.actions.get(action[2]['object'].exec()) for action in self.action_plan]
        return 'Action planning execution results: {}'.format(self.action_plan_response)

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
    acting.upon(sense, enter=sensing, outputs=[__reset_working_memory, __sense])
    # change orders
    waiting_orders.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    planning.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    acting.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    # reset working memory from sensing
    sensing.upon(wait, enter=waiting_orders, outputs=[__reset_working_memory])


class AutomatonController(object):

    def __init__(self, actions: Actions, sensors: Sensors, name: str, world_state: dict):
        self.automaton = Automaton(actions=actions, sensors=sensors, name=name, world_state=world_state)

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
                print('World state differs from goal: \nState: {}\nGoal: {}'.format(self.automaton.world_state, self.goal))
                print('Need to find an action plan')
                self.automaton.plan()
                print('Plain found. Will execute the action plan: {}'.format(self.automaton.action_plan))
                self.automaton.act()
            else:
                print('World state equals to goal: {}'.format(self.goal))
                self.automaton.wait()
            sleep(5)

