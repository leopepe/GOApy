# from Goap.Action import ActionResponse
from typing import Callable, List, Optional
from Goap.Errors import ActionAlreadyInCollectionError


class Action:
    def __init__(
            self,
            func: Callable,
            name: str,
            pre_conditions: dict,
            effects: dict,
            cost: float = 0.1):
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
        if len(self.__dict__) < len(other.__dict__):
            return -1
        elif len(self.__dict__) > len(other.__dict__):
            return 1
        else:
            return 0

    def __hash__(self):
        return hash(self)

    def __call__(self):
        return self.exec()

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response

    async def async_exec(self):
        return await self.func()

    def exec(self):
        try:
            stdout, stderr, return_code = self.func()
        except RuntimeError as e:
            raise RuntimeError(
                f"Error executing function {self.func}. Exception: {e}"
            )
        self.response = ActionResponse(
            stdout=stdout,
            stderr=stderr,
            return_code=return_code
        )
        return self.response


class ActionResponse:
    def __init__(
        self,
        stdout: str = '',
        stderr: str = '',
        return_code: int = 0,
        trim_chars: str = '\r\n',
    ):
        """

        :param return_code:
        :param stdout:
        :param stderr:
        """
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code
        self.trim_chars = trim_chars
        self.response = None

    def __call__(self):
        return self.response

    def __str__(self):
        return f'{self.response}'

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def __trim(string: str):
        return string.strip('\r\n')

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, value: str):
        self._stdout = self.__trim(value)

    @property
    def stderr(self):
        return self._stderr

    @stderr.setter
    def stderr(self, value: str):
        self._stderr = self.__trim(value)

    @property
    def return_code(self):
        return self._return_code

    @return_code.setter
    def return_code(self, value: int):
        self._return_code = value

    @property
    def response(self):
        if self.stdout:
            return self.stdout
        elif self.stderr:
            return self.stderr

    @response.setter
    def response(self, value):
        self._response = value


class Actions:

    def __init__(self, actions: Optional[List[Action]] = []):
        self.actions = actions

    def __str__(self):
        names = [action.name for action in self.actions]
        return '{}'.format(names)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self.actions

    def __len__(self):
        if self.actions:
            return len(self.actions)
        else:
            return 0

    def __getitem__(self, key: str) -> Optional[Action]:
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

    def get_by_pre_conditions(
            self,
            pre_conditions: dict) -> Optional[List[Action]]:
        result = []
        for action in self.actions:
            if action.pre_conditions == pre_conditions:
                result.append(action)
        return result

    def get_by_effects(
            self,
            effects: dict) -> Optional[List[Action]]:
        result = []
        for action in self.actions:
            if action.effects == effects:
                result.append(action)
        return result

    def add(
            self,
            name: str,
            pre_conditions: dict,
            effects: dict,
            func: Callable,
            cost: float = 0.1):
        if self.get(name):
            raise ActionAlreadyInCollectionError(
                f"The action name {name} is already in use"
            )
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

    def run_all(self) -> list:
        responses = []
        for action in self.actions:
            action.exec()
            responses.append(action.response)
        return responses

    # async def async_run(self):
    #     response = []
    #     for action in self.actions:
    #         await response.append(action.async_exec())

    @staticmethod
    def compare_actions(action1: Action, action2: Action) -> bool:
        result = False
        if (
            action1.pre_conditions == action2.pre_conditions
            and action1.effects == action2.effects

        ):
            result = True

        return result
