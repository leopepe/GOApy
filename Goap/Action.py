# from Goap.Action import ActionResponse
from typing import Callable, List, Optional
from filecmp import cmp

from Goap.Errors import ActionMultipleTypeError, ActionAlreadyInCollectionError


class Action:
    def __init__(
            self,
            func: Callable,
            name: str,
            pre_conditions: dict,
            effects: dict,
            cost: float):
        self.func = func
        self.name = name
        self.pre_conditions = pre_conditions
        self.effects = effects
        self.cost = cost
        self._response: Optional[ActionResponse] = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self, other)

    def __hash__(self):
        return hash(self)

    def __call__(self, **kwargs):
        self.exec()

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self,
                 stdout: str,
                 stderr: str,
                 return_code: str,
                 trim_chars: str
                 ):
        self._response = ActionResponse(
            trim_chars=trim_chars,
            stdout=stdout,
            stderr=stderr,
            return_code=return_code
        )

    def exec(self):
        try:
            self.func()
        except RuntimeError as e:
            raise RuntimeError(
                f"Error executing function {self.func}. Exception: {e}"
            )


class ActionResponse:

    def __init__(
            self,
            trim_chars: str = '',
            return_code: str = '0',
            stdout: str = '',
            stderr: str = ''):
        """

        :param name:
        :param action_type:
        :param return_code:
        :param stdout:
        :param stderr:
        """
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.trim_chars = trim_chars
        self.__response_parser()

    def __repr__(self):
        return self.__str__()

    def __response_parser(self):
        if not self.stdout == '':
            self.response = self.stdout
        elif not self.stderr == '':
            self.response = self.stderr

    def __str__(self):
        return f'Response: {self.response}, ReturnCode: {self.return_code}'

    def __trim(self, string: str):
        return string.strip(self.trim_shars)

    @ property
    def stdout(self):
        return self._stdout

    @ stdout.setter
    def stdout(self, value: str):
        self._stdout = self.__trim(value)

    @ property
    def stderr(self):
        return self._stderr

    @ stderr.setter
    def stderr(self, value: str):
        self._stderr = self.__trim(value)

    @ property
    def response(self):
        if self.stdout:
            return self.stdout
        elif self.stderr:
            return self.stderr


class Actions:

    def __init__(self, actions: Optional[List[Action]] = []):
        self.actions = actions

    def __str__(self):
        return '{}'.format(self.actions)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.actions)

    def __len__(self):
        return len(self.actions)

    """
    def __cmp__(self, other: Action):
        pass


    def __contains__(self, other: Action):
        # if not self.get(other.name)
        pass
    """

    def __getitem__(self, key: str):
        for action in self.actions:
            if action.name == key:
                return action
            else:
                return None

    def get(self, name: str = None) -> Optional[Action]:
        result = None
        for action in self.actions:
            if action.name == name:
                result = action
        return result

    def get_by_pre_condition(self, pre_conditions: dict) -> Optional[Action]:
        result = None
        for action in self.actions:
            if action.pre_conditions == pre_conditions:
                result = action
        return result

    def get_by_effect(self, effects: dict):
        for action in self.actions:
            if action.effects == effects:
                return action

    def add(self, name: str, pre_conditions: dict, effects: dict, cost: float, func: Callable):
        self.actions.append(
            Action(func, name, pre_conditions, effects, cost)
        )

    def remove(self, name: str):
        result = False
        for action in self.actions:
            if action.name == name:
                self.actions.remove(action)
                result = True
        return result

    async def run_all(self) -> list:
        responses = []
        for action in self.actions:
            await action.exec()
            responses.append(action.response)
        return responses

    @staticmethod
    def compare_actions(action1: Action, action2: Action):
        result = None
        if action1.pre_conditions == action2.pre_conditions and action1.effects == action2.effects:
            result = 'Action {} and Action {} are equal'.format(
                action1.name, action2.name)

        return result
