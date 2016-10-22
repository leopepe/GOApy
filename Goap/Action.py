from json import dumps


class Action:

    def __init__(self, name: str, pre_conditions: dict, effects: dict):
        self.name = name
        self.pre_conditions = pre_conditions
        self.effects = effects

    def do(self):
        pass

    def chain(self, obj):
        if self.pre_conditions == obj.effects:
            return True

    def __str__(self):
        return dumps({'Name': self.name, 'Conditions': self.pre_conditions, 'Effects': self.effects})

    def __repr__(self):
        return self.__str__()


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

    def add_action(self, name, pre_conditions, effects):
        # add action to self.actions
        self.actions.append(Action(name, pre_conditions, effects))

    def remove_action(self, name: str):
        # traverse self.actions and remove named action
        [self.actions.remove(action) for action in self.actions if action.name == name]

    def get(self, name):
        result = [action for action in self.actions if action.name == name]
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

    def list_all_states(self):
        pre_conditions = [action.pre_conditions for action in self.actions]
        effects = [action.effects for action in self.actions]
        unique = set(pre_conditions + effects)
        all_states = unique
        return all_states


if __name__ == '__main__':
    # ACTIONS
    actions = Actions()
    # VPC/Network set
    actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # DB set
    actions.add_action(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    actions.add_action(
        name='StopDB',
        pre_conditions={'vpc': True, 'db': 'started', 'app': False},
        effects={'vpc': True, 'db': 'stopped', 'app': False}
    )
    actions.add_action(
        name='StartDB',
        pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
        effects={'vpc': True, 'db': 'started', 'app': False}
    )
    actions.add_action(
        name='DestroyDB',
        pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # APP set
    actions.add_action(
        name='CreateApp',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': True, 'app': True}
    )
    actions.add_action(
        name='StartApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': 'started'}
    )
    actions.add_action(
        name='StopApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
        effects={'vpc': True, 'db': True, 'app': 'stopped'}
    )
    actions.add_action(
        name='DestroyApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    print('{0}\n{1}'.format(actions, actions.__len__()))
    actions.remove_action(name='CreateVPC')
    print('{0}\n{1}'.format(actions, actions.__len__()))
    print(actions.get(name='CreateDB'))
    print(actions.list_all_states())
