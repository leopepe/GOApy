from automat import MethodicalMachine
from Goap.Sensor import Sensors, SensorResponse
from Goap.Action import Actions
from Goap.Planner import Planner


class AutomatonPriorities:
    def __init__(self, items):
        self._items = items

    def __iter__(self):
        return self._items

    def __call__(self):
        return next(self._items.read())


class Automaton:
    """ A 3 State Machine Automaton: observing (aka monitor or patrol), planning and acting

    """

    machine = MethodicalMachine()

    def __init__(self, name: str='Automaton', sensors: Sensors=[], actions: Actions=[]):
        self.name = name
        # known facts about the environment/world
        self.knowledge = {}
        # recognized env/world state
        self.env_state = {}
        self.sensors = sensors
        self.actions = actions
        self.planner = Planner(actions=actions)
        self.action_plan = []
        self.action_plan_response = None
        self.sensors_responses = {}
        self.actions_response = []
        self.goal = {}

    def __execute_sensors(self):
        """ Invoke __convert_responses_into_knowledge to parse acknowledge the world state """
        # execute the sensors
        try:
            return self.sensors.exec_all()
        except IOError as err:
            raise 'Error executing sensors: {}'.format(err)

    def __convert_responses_into_knowledge(self, responses: list):
        for r in responses:
            self.sensors_responses.update({r.name: r.output})
        return 'The environment goal: {}'.format(self.sensors_responses)

    @machine.state(initial=True)
    def idle(self):
        """ Machine is on but waiting orders"""

    @machine.input()
    def input_goal(self, goal):
        """ """

    @machine.output()
    def __set_goal(self, goal):
        """ Set Automaton's goal """
        try:
            self.goal = goal
        except IOError as err:
            raise 'Error setting the goal {}'.format(err)

        # execute sensors and collect data
        responses = self.sensors.exec_all()
        try:
            self.__convert_responses_into_knowledge(responses=responses)
        except IOError as err:
            raise 'Error converting JSON data into Automatons knowledge {}'.format(err)

    @machine.state()
    def observing(self):
        """ The automaton monitors/patrol the environment waiting for an event """

    @machine.output()
    def __report_all(self):
        if self.env_state != self.goal:
            status = False
        else:
            status = True
        return {
            'env_state': self.env_state,
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
        self.action_plan = self.planner.plan(self.env_state, self.goal)
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
    from pprint import PrettyPrinter
    from json import loads
    # Instantiate
    pp = PrettyPrinter(indent=4)
    priorities = AutomatonPriorities([
        {'vpc': {'State':'available'}, 'db': {'DBInstanceStatus': 'available'}, 'app': {'Status': {'Code': 16, 'Name': 'running'}}},
        {'vpc': 'monitored', 'db': 'monitored', 'app': 'monitored'}
    ])
    aws_actions = Actions()
    aws_actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    aws_actions.add_action(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    aws_sensors = Sensors()
    aws_sensors.add(name='FindProjectVPC', shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].{VpcId:VpcId,State:State,Tags:Tags[*]}" --output json')
    aws_sensors.add(name='FindProjectDB', shell='aws rds describe-db-instances --query "DBInstances[].{Name:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus}" --output json')
    aws_sensors.add(name='FindProjectInstances', shell='aws ec2 describe-instances --filters "Name=tag-key,Values=project","Name=tag-value,Values=mesos-master" --query "Reservations[].Instances[].{Name:KeyName,Status:State,InstanceId:InstanceId,InstanceType:InstanceType,ImageId:ImageId}"')
    ai = Automaton(name='infra_builder', actions=aws_actions, sensors=aws_sensors)
    # Control
    # what is the environment status? what does the sensors return? ai has a goal?
    # goal = priorities # object not working returning object rather then dict
    goal = {'vpc': {'State':'available'}, 'db': {'DBInstanceStatus': 'available'}, 'app': {'Status': {'Code': 16, 'Name': 'running'}}}
    recon_world = ai.input_goal(goal)
    action_plan = ai.plan()
    result = ai.execute_plan()
    pp.pprint('{}, {}, {}'.format(recon_world, action_plan, result))
    pp.pprint(ai.report())



