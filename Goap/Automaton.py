from datetime import datetime
from automat import MethodicalMachine
from Goap.Sensor import Sensors, SensorResponse
from Goap.Action import Actions
from Goap.Planner import Planner
from rx import Observable, Observer


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


WORLD_STATE = WorldState({
    'vpc_state': 'Unknown',
    'pub_subnet': 'Unknown',
    'prv_subnet': 'Unknown',    # True || False
    'db_state': 'Unknown',      # True || False
    'instances_state': 'Unknown',     # True || False
})

WORKING_MEMORY = []


class AutomatonPriorities:

    def __init__(self, items: list):
        self._items = items

    def __iter__(self):
        return self._items

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return self.__repr__()


class SensorResponseToFact(Observer):

    def on_next(self, sensor):
        WORKING_MEMORY.append(Fact(sensor=sensor.name, data=sensor.exec(), binding=sensor.binding))

    def on_error(self, error):
        return 'Error: {}'.format(error)

    def on_completed(self):
        return 'Done!'


class AssimilateFact(Observer):

    def on_next(self, fact):
        setattr(WORLD_STATE, fact.binding, fact.data.output)

    def on_error(self, error):
        return 'Error: {}'.format(error)

    def on_completed(self):
        return 'Done!'


class Automaton:
    """ A 3 State Machine Automaton: observing (aka monitor or patrol), planning and acting

    # debug
    Observable.from_(sensors).subscribe(lambda sensor: print('Sensor: {}'.format(sensor)))
    # Process Sensors and Transform it into fact on the  WORKING_MEMORY
    Observable.from_(sensors).subscribe(SensorResponseToFact())
    # debug
    Observable.from_(WORKING_MEMORY).subscribe(lambda response: print('Fact: {}, Binding: {}'.format(response, response.binding)))
    # update world state vpc_state
    Observable.from_(WORKING_MEMORY).subscribe(AssimilateFact())

    print(WORKING_MEMORY)
    print(WORLD_STATE)

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

    def __sense_environment(self):
        Observable.from_(self.sensors).subscribe(SensorResponseToFact())
        Observable.from_(WORKING_MEMORY).subscribe(AssimilateFact())

    @staticmethod
    def get_world_state():
        return WORLD_STATE

    @machine.state(initial=True)
    def idle(self):
        """ Machine is ON and waiting for orders/goal """

    @machine.input()
    def input_goal(self, goal):
        """ Input goal """

    @machine.output()
    def __set_goal(self, goal):
        """ Set Automaton's goal """
        self.goal = goal
        try:
            self.__sense_environment()
        except IOError as err:
            raise 'Error converting JSON data into Automatons knowledge {}'.format(err)

    @machine.state()
    def observing(self):
        """ The automaton monitors/patrol the environment waiting for an event """

    @machine.output()
    def __report_all(self):
        if WORLD_STATE != self.goal:
            status = False
        else:
            status = True
        return {
            'env_state': WORLD_STATE,
            'goal': self.goal,
            'status': status,
            'last_plan': self.action_plan,
            'last_actions_results': self.action_plan_response
        }

    @machine.state()
    def planning(self):
        """ Planing a sequence of actions to change the environment """

    @machine.input()
    def plan(self):
        """ Create a plan """

    @machine.output()
    def __formulate_action_plan(self):
        self.action_plan = self.planner.plan(WORLD_STATE, self.goal)
        return self.action_plan

    @machine.state()
    def acting(self):
        """ Changing the environment """

    @machine.input()
    def execute_plan(self):
        """ Change the environment """

    @machine.input()
    def goal_achieved(self):
        """ Goal achieved """

    @machine.output()
    def __execute_action_plan(self):
        self.actions_response = [action() for action in self.action_plan]
        return 'Action planning execution results: {}'.format(self.action_plan_response)

    @machine.output()
    def __get_action_plan_result(self):
        return self.actions_response

    @machine.input()
    def report(self):
        """ Report actual knowledge and world state """

    # idle -> observing [run sensors, return senors data]
    idle.upon(input_goal, enter=observing, outputs=[__set_goal])
    observing.upon(input_goal, enter=observing, outputs=[__set_goal])
    observing.upon(report, enter=observing, outputs=[__report_all])
    observing.upon(plan, enter=planning, outputs=[__formulate_action_plan])
    planning.upon(execute_plan, enter=acting, outputs=[__execute_action_plan])
    planning.upon(report, enter=planning, outputs=[__report_all])
    acting.upon(goal_achieved, enter=idle, outputs=[__report_all])
    acting.upon(report, enter=acting, outputs=[__report_all])


if __name__ == '__main__':
    """ Proposed env_state:
    
        {
            "Vpc": {
                "state": "available|doesnt_exist"
            },
            "Network": {
                "private_subnet": false|true,
                "public_subnet": false|true,
                "internet_access": false|true,
                "access_to_vpn": "yes|no",
                "route_to_vpcs": ["vpn_2_office", "vpn_2_customer", ...]
            },
            "DB": {
                "state": "available|doesnt_exist|"
            }
            "App": {
                "type": "asg|instance",
                "state": "available|doesnt_exist",
                "node_count": 0
            }
        }

    
    """
    from pprint import PrettyPrinter
    # from json import loads
    # Instantiate
    pp = PrettyPrinter(indent=4)
    priorities = AutomatonPriorities([
        {'vpc_state': 'available', 'db_state': 'available', 'instances_state': 'running'}
    ])
    aws_actions = Actions()
    aws_actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc_state': False, 'db_state': False, 'instances_state': False},
        effects={'vpc_state': True, 'db_state': False, 'instances_state': False}
    )
    aws_actions.add_action(
        name='CreateDB',
        pre_conditions={'vpc_state': 'available', 'db_state': False, 'instances_state': False},
        effects={'vpc_state': 'available', 'db_state': 'available', 'instances_state': False}
    )
    aws_sensors = Sensors()
    aws_sensors.add(
        name='FindProjectVPC',
        shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].State" --output text',
        binding='vpc_state'
    )
    aws_sensors.add(
        name='FindProjectDB',
        shell='aws rds describe-db-instances --filters "Name=db-instance-id,Values=rds-oraculo" --query "DBInstances[].DBInstanceStatus" --output text',
        binding='db_state'
    )
    aws_sensors.add(
        name='FindProjectInstances',
        shell='aws ec2 describe-instances --filters "Name=tag-key,Values=project","Name=tag-value,Values=mesos-master" --query "Reservations[].Instances[].State" --output text|awk \'{print $2}\'',
        binding='instances_state'
    )
    ai = Automaton(name='infra_builder', actions=aws_actions, sensors=aws_sensors)
    # Control
    # what is the environment status? what does the sensors return? ai has a goal?
    # goal = priorities # object not working returning object rather then dict
    goal = {'vpc_state': 'available', 'db_state': 'available', 'instances_state': 'running'}
    recon_world = ai.input_goal(goal)
    action_plan = ai.plan()
    result = ai.execute_plan()
    pp.pprint('Acknowledge world: {}, Action Plan: {}, Result: {}'.format(recon_world, action_plan, result))
    pp.pprint(ai.report())

