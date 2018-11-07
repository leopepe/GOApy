from datetime import datetime
from automat import MethodicalMachine
from Goap.Sensor import Sensors
from Goap.Action import Actions
from Goap.Planner import Planner
from rx import Observable

DEFAULT_WORLD_STATE = {
    'vpc_state': 'Unknown',
    'pub_subnet': 'Unknown',
    'prv_subnet': 'Unknown',    # True || False
    'db_state': 'Unknown',      # True || False
    'app_state': 'Unknown',     # True || False
}


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

    def __init__(self, name: str='Automaton', sensors: Sensors=[], actions: Actions=[],
                 world_state: dict=DEFAULT_WORLD_STATE):
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

    # cyclical main states
    waiting_orders.upon(sense, enter=sensing, outputs=[__sense])
    sensing.upon(plan, enter=planning, outputs=[__plan])
    planning.upon(act, enter=acting, outputs=[__act])
    acting.upon(sense, enter=sensing, outputs=[__sense])
    # change orders
    waiting_orders.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    planning.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])
    acting.upon(input_goal, enter=waiting_orders, outputs=[__input_goal])


if __name__ == '__main__':
    """ proposed world_state:
    
        world_state_matrix = {
            "vpc_state": 'Unknown',
            "private_subnet": 'Unknown',
            "public_subnet": 'Unknown',
            "internet_access": 'Unknown',
            "access_to_vpn": 'Unknown',
            "db_state": 'Unknown',
            "db_type": 'Unknown',
            "app_state": 'Unknown',
            "app_type": 'Unknown',
            "node_count": 0
    }
    
    """

    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    priorities = AutomatonPriorities([
        {'vpc_state': 'available', 'db_state': 'available', 'app_state': 'running'}
    ])
    world_state_matrix = {
        "vpc_state": 'Unknown',
        "db_state": 'Unknown',
        "app_state": 'Unknown',
    }
    goal = {
        "vpc_state": "available",
        "db_state": "available",
        "app_state": "running",
    }
    aws_actions = Actions()
    aws_actions.add(
        name='CreateVPC',
        pre_conditions={'vpc_state': 'unavailable', 'db_state': 'unavailable', 'app_state': 'unavailable'},
        effects={'vpc_state': 'available', 'db_state': 'unavailable', 'app_state': 'unavailable'},
        shell='echo "vpc created"'
    )
    aws_actions.add(
        name='CreateDB',
        pre_conditions={'vpc_state': 'available', 'db_state': 'unavailable', 'app_state': 'unavailable'},
        effects={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'unavailable'},
        shell='echo "db created"'
    )
    aws_actions.add(
        name='CreateApp',
        pre_conditions={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'unavailable'},
        effects={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'running'},
        shell='echo "app created" > /tmp/CreateApp.out'
    )
    aws_sensors = Sensors()
    aws_sensors.add(
        name='FindProjectVPC',
        # shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].State" --output text',
        shell='echo -n "unavailable"',
        binding='vpc_state'
    )
    aws_sensors.add(
        name='FindProjectDB',
        # shell='aws rds describe-db-instances --filters "Name=db-instance-id,Values=rds-oraculo" --query "DBInstances[].DBInstanceStatus" --output text',
        shell='echo -n "unavailable"',
        binding='db_state'
    )
    aws_sensors.add(
        name='CheckAppState',
        shell='echo -n "unavailable"',
        binding='app_state'
    )
    ai = Automaton(name='infra_builder', actions=aws_actions, sensors=aws_sensors, world_state=world_state_matrix)
    # Control
    # what is the environment status? what does the sensors return? ai has a goal?
    # goal = priorities # object not working returning object rather then dict
    ai.input_goal(goal)
    ai.sense()
    pp.pprint(
        'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(ai.world_state, ai.action_plan, ai.actions_response)
    )
    ai.plan()
    ai.act()
    pp.pprint(
        'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(ai.world_state, ai.action_plan, ai.actions_response)
    )

