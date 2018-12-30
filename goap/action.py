import subprocess
from filecmp import cmp
from json import dumps

from goap.errors import *


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

    def __call__(self, **kwargs):
        self.__init__(kwargs.get('name'), kwargs.get('pre_conditions'), kwargs.get('effects'))
        self.exec()

    def exec(self) -> tuple:
        pass


class ActionResponse:

    def __init__(self, name: str, action_type: str, return_code: str, stdout: str='', stderr: str=''):
        """
        
        :param name: 
        :param action_type: 
        :param return_code: 
        :param stdout: 
        :param stderr: 
        """
        self.name = name
        self.action_type = action_type
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.__response_parser()

    def __str__(self):
        return 'Name: {}, Response: {}, ReturnCode: {}'.format(self.name, self.response, self.return_code)

    def __repr__(self):
        return self.__str__()

    def __response_parser(self):
        if not self.stdout == '':
            self.response = self.stdout
        elif not self.stderr == '':
            self.response = self.stderr


class ShellAction(Action):

    def __init__(self, name: str, pre_conditions: dict, effects: dict, shell: str):
        self.response = {}
        self.type = 'shell'
        self.shell = shell
        Action.__init__(self, name=name, pre_conditions=pre_conditions, effects=effects)

    def __repr__(self):
        return 'Name: {}'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def exec(self):
        cmd = self.shell
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        try:
            stdout, stderr = process.communicate(timeout=30)
            return_code = process.returncode
            self.response = ActionResponse(
                name=self.name,
                action_type='shell',
                stdout=stdout,
                stderr=stderr,
                return_code=return_code
            )
        except TimeoutError as e:
            process.kill()
            raise('{}'.format(e))
        finally:
            process.kill()

        return self.response


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

    def __add_shell_action(self, name, shell, pre_conditions, effects):
        if not ShellAction(name=name, shell=shell, pre_conditions=pre_conditions, effects=effects) in self.actions:
            self.actions.append(ShellAction(name=name, shell=shell, pre_conditions=pre_conditions, effects=effects))
        else:
            raise actionAlreadyInCollectionError

    def __add_obj_action(self, name, obj, pre_conditions, effects):
        raise NotImplementedError

    def add(self, **kwargs):
        if kwargs.get('shell') and kwargs.get('obj'):
            raise ActionMultipleTypeError

        name = kwargs.get('name')
        shell = kwargs.get('shell', None)
        obj = kwargs.get('obj', None)
        pre_conditions = kwargs.get('pre_conditions', None)
        effects = kwargs.get('effects', None)
        if shell:
            self.__add_shell_action(name, shell, pre_conditions, effects)
        elif obj:
            self.__add_obj_action(name, obj, pre_conditions, effects)

    def remove(self, name: str):
        result = False
        for action in self.actions:
            if action.name == name:
                self.actions.remove(action)
                result = True
        return result

    def exec_all(self) -> list:
        responses = [s.exec() for s in self.actions]
        return responses

    @staticmethod
    def compare_actions(action1: Action, action2: Action):
        result = None
        if action1.pre_conditions == action2.pre_conditions and action1.effects == action2.effects:
            result = 'Action {} and Action {} are equal'.format(action1.name, action2.name)

        return result


if __name__ == '__main__':
    # ACTIONS
    aws_actions = Actions()
    # VPC/Network set
    aws_actions.add(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False},
        shell='awscli --help'
    )
    # DB set
    aws_actions.add(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False},
        shell='awscli --help'
    )
    aws_actions.add(
        name='StopDB',
        pre_conditions={'vpc': True, 'db': 'started', 'app': False},
        effects={'vpc': True, 'db': 'stopped', 'app': False},
        shell='awscli --help'
    )
    aws_actions.add(
        name='StartDB',
        pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
        effects={'vpc': True, 'db': 'started', 'app': False},
        shell='awscli --help'
    )
    aws_actions.add(
        name='DestroyDB',
        pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
        effects={'vpc': True, 'db': False, 'app': False},
        shell='awscli --help'
    )
    # APP set
    aws_actions.add(
        name='CreateApp',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': True, 'app': True},
        shell='awscli --help'
    )
    aws_actions.add(
        name='StartApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': 'started'},
        shell='awscli --help'
    )
    aws_actions.add(
        name='StopApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
        effects={'vpc': True, 'db': True, 'app': 'stopped'},
        shell='awscli --help'
    )
    aws_actions.add(
        name='DestroyApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
        effects={'vpc': True, 'db': True, 'app': False},
        shell='awscli --help'
    )
    print('{0}\n{1}'.format(aws_actions, aws_actions.__len__()))
    aws_actions.remove(name='CreateVPC')
    print('{0}\n{1}'.format(aws_actions, aws_actions.__len__()))
    print(aws_actions.get(name='CreateDB'))
    # action.do() returns a tuple
    print(type(aws_actions.get(name='CreateDB')), aws_actions.get(name='CreateDB'))
    fs_actions = Actions()
    fs_actions.add(
        name='CompactBigLogFiles',
        pre_conditions={'files_to_compact': 'Exists'},
        effects={'files_to_compact': 'None'},
        shell='find /tmp -name "*.log" -type f -size +900M| xargs tar -zcvf logfile-$(date "+%d%m%y-%H%M%S").tar.gz {}'
    )
    print(fs_actions)

