from filecmp import cmp
from json import dumps


class ActionResponse:
    def __init__(self, **kwargs):
        self.sensor_type = kwargs.get('type', None)
        self.sensor_response = self.__adapt_response(**kwargs)

    def __adapt_response(self, **kwargs):
        if self.sensor_type == 'shell':
            response = ShellCommandResponse(**kwargs)
        elif self.sensor_type == 'awsapi':
            response = AWSCommandResponse(**kwargs)
        else:
            raise '{} Need to specify the sensor\'s type'.format(ActionError)
        return response


class ShellCommandResponse:
    """ ShellCommand Return is a class for represent the agent's actions return """

    def __init__(self, **kwargs):
        """

        :rtype: object
        :param kwargs: return_code, output and error
        """
        self.name = kwargs.get('name', None)
        self.return_code = kwargs.get('return_code', None)
        self.output = str(kwargs.get('output', None)).replace('\n', '').replace('\t', '')
        self.error = kwargs.get('error', None).replace('\n', '').replace('\t', '')

    def __return_message(self):
        if self.return_code == 0 and self.__check_response():
            return {'return_code': self.return_code, 'output': str(self.output).replace('\n', '').replace('\t', '')}
        elif self.return_code == 0 and not self.__check_response():
            return {'return_code': self.return_code, 'error': str('False')}
        else:
            return {'return_code': self.return_code, 'error': str(self.error).replace('\n', '').replace('\t', '')}

    def __check_response(self):
        if self.output == '' or self.output == '\n':
            return False
        else:
            return True

    def __repr__(self):
        return str(self.__return_message())

    def __str__(self):
        return self.__repr__()


class ShellCommand:
    """ Shell Sensor object factory

    """

    def __init__(self, name: str, pre_conditions: dict, effects: dict, shell: str):
        """ *nix shell Command

        """
        self.name = name
        self.pre_conditions = pre_conditions
        self.effects = effects
        self.type = 'shell'
        self.shell = shell
        self.return_code = None
        self.stdout = None
        self.stderr = None
        self.response = {}

    def __repr__(self):
        return 'Name: {}'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def exec(self):
        """ Executes the sensor. Sensor's can be objects or a cli command

        :return SensorResponse:
        """
        cmd = self.shell
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        try:
            stdout, stderr = proc.communicate(timeout=30)
            returncode = proc.returncode
            self.response = ShellCommandResponse(name=self.name, output=stdout, error=stderr, return_code=returncode)
        except TimeoutError as e:
            proc.kill()
            raise('{}'.format(e))

        return self.response


class AWSCommandResponse:
    """ CommandReturn is a class for represent the agent's sensor's return """

    def __init__(self, **kwargs):
        """

        :param kwargs: expects response as dict argument and parse aws http response
        """
        self.return_code = None
        self.output = None
        self.error = None
        self.name = kwargs.get('name', None)
        self.sensor_response = kwargs.get('response', None)
        self._json_parsed_response = None

        self.__parse_aws_api_http_response()

    def __parse_aws_api_http_response(self):
        self._json_parsed_response = json.loads(self.sensor_response)
        self.return_code = self._json_parsed_response['ResponseMetadata']['HTTPStatusCode']
        if self.return_code == '200':
            self.output = self._json_parsed_response
        else:
            self.error = self._json_parsed_response

    def __repr__(self):
        json_data = {}
        if self.output:
            json_data = {'return_code': self.return_code, 'output': str(self.output)}
        elif self.error:
            json_data = {'return_code': self.return_code, 'error': str(self.error)}
        return json.dumps(json_data, skipkeys=True)

    def __str__(self):
        return self.__repr__()


class Action:

    def __init__(self, name: str, pre_conditions: dict, effects: dict):
        self.name = name
        self.pre_conditions = pre_conditions
        self.effects = effects

    def __str__(self):
        # return dumps({'Name': self.name, 'Conditions': self.pre_conditions, 'Effects': self.effects})
        return dumps({'Name': self.name})

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self, other)

    def __hash__(self):
        return hash(self)

    def __call__(self):
        pass

    def exec(self) -> tuple:
        # print(self.name)
        return self.name, True


class Actions:

    def __init__(self):
        self.actions = list()

    def __str__(self):
        return '{}'.format(self.actions)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.actions)

    def __len__(self):
        return len(self.actions)

    def __getitem__(self, key):
        for a in self.actions:
            if a.name == key:
                return a
            else:
                return None

    def add(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        if kwargs.get('shell') and kwargs.get('obj'):
            raise ActionMultipleTypeError

        name = kwargs.get('name')
        pre_conditions = kwargs.get('pre_conditions')
        effects = kwargs.get('effects')
        shell = kwargs.get('shell', None)
        obj = kwargs.get('obj', None)
        binding = kwargs.get('binding', None)
        if shell:
            self.add_shell_command(name, pre_conditions, effects, shell)
        elif obj:
            self.add_obj_command(name, obj, binding)

    def add_shell_command(self, name, pre_conditions, effects, shell):
        # add action to self.actions
        self.actions.append(ShellCommand(name, pre_conditions, effects, shell))

    def remove(self, name: str):
        # traverse self.actions and remove named action
        [self.actions.remove(action) for action in self.actions if action.name == name]

    def get(self, name):
        result = None
        for action in self.actions:
            if action.name == name:
                result = action
        return result

    def get_action_by_pre_condition(self, pre_conditions):
        result = [action for action in self.actions if action.pre_conditions == pre_conditions]
        return result

    def all_possible_states(self):
        state_grid = []
        for a in self.actions:
            if a.pre_conditions not in state_grid:
                state_grid.append(a.pre_conditions)
            if a.effects not in state_grid:
                state_grid.append(a.effects)
        return state_grid

    @staticmethod
    def compare_actions(action1: Action, action2: Action):
        result = None
        if action1.pre_conditions == action2.pre_conditions and action1.effects == action2.effects:
            result = 'Action {} and Action {} are equal'.format(action1.name, action2.name)

        return result


if __name__ == '__main__':
    # ACTIONS
    actions = Actions()
    # VPC/Network set
    actions.add(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # DB set
    actions.add(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    actions.add(
        name='StopDB',
        pre_conditions={'vpc': True, 'db': 'started', 'app': False},
        effects={'vpc': True, 'db': 'stopped', 'app': False}
    )
    actions.add(
        name='StartDB',
        pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
        effects={'vpc': True, 'db': 'started', 'app': False}
    )
    actions.add(
        name='DestroyDB',
        pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # APP set
    actions.add(
        name='CreateApp',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': True, 'app': True}
    )
    actions.add(
        name='StartApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': 'started'}
    )
    actions.add(
        name='StopApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
        effects={'vpc': True, 'db': True, 'app': 'stopped'}
    )
    actions.add(
        name='DestroyApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    print('{0}\n{1}'.format(actions, actions.__len__()))
    actions.remove(name='CreateVPC')
    print('{0}\n{1}'.format(actions, actions.__len__()))
    print(actions.get(name='CreateDB'))
    # action.do() returns a tuple
    print(type(actions.get(name='CreateDB').do()), actions.get(name='CreateDB').do())
