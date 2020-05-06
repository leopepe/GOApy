import subprocess
from filecmp import cmp

from Goap.Errors import *


class Action:

    def __init__(
            self,
            name: str,
            pre_conditions: dict,
            effects: dict,
            cost: float):
        self.name = name
        self.pre_conditions = pre_conditions
        self.effects = effects
        self.cost = cost

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self, other)

    def __hash__(self):
        return hash(self)

    def __call__(self, **kwargs):
        self.__init__(
            kwargs.get('name'),
            kwargs.get('pre_conditions'),
            kwargs.get('effects'))
        self.exec()

    def exec(self) -> tuple:
        pass


class ActionResponse:

    def __init__(
            self,
            name: str,
            action_type: str,
            return_code: str,
            stdout: str = '',
            stderr: str = ''):
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
        return 'Name: {}, Response: {}, ReturnCode: {}'.format(
            self.name, self.response, self.return_code)

    def __repr__(self):
        return self.__str__()

    def __response_parser(self):
        if not self.stdout == '':
            self.response = self.stdout
        elif not self.stderr == '':
            self.response = self.stderr


class ShellAction(Action):

    def __init__(
            self,
            name: str,
            pre_conditions: dict,
            effects: dict,
            shell: str,
            cost: float = 0.0):
        self.response = {}
        self.type = 'shell'
        self.shell = shell
        Action.__init__(
            self,
            name=name,
            pre_conditions=pre_conditions,
            effects=effects,
            cost=cost)

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

    def get_by_pre_condition(self, pre_conditions: dict):
        for action in self.actions:
            if action.pre_conditions == pre_conditions:
                return action

    def get_by_effect(self, effects: dict):
        for action in self.actions:
            if action.effects == effects:
                return action

    def __add_shell_action(self, name, shell, pre_conditions, effects):
        if not ShellAction(
                name=name,
                shell=shell,
                pre_conditions=pre_conditions,
                effects=effects) in self.actions:
            self.actions.append(
                ShellAction(
                    name=name,
                    shell=shell,
                    pre_conditions=pre_conditions,
                    effects=effects))
        else:
            raise ActionAlreadyInCollectionError

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
            result = 'Action {} and Action {} are equal'.format(
                action1.name, action2.name)

        return result
