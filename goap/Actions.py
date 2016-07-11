# from collections import deque


class Action:

    def __init__(self, name: str, pre_conditions: list, post_effects: list, negative_effects: list):
        self.name = name
        self.pre_conditions = pre_conditions
        self.post_effects = post_effects
        self.neg_effects = negative_effects

    @property
    def effects(self):
        return self.post_effects

    @property
    def counter_effects(self):
        return self.neg_effects

    def __str__(self):
        return 'Action: {0}, {1}'.format(self.name, self.__dict__)

    def __repr__(self):
        return self.__str__()

    def do(self):
        """" Overwrite this to include a real execution """
        pass

    def undo(self):
        """ Undo action (???) """
        pass

    def satisfy_preconditions(self, facts: list):
        """ The actions must satisfy it' preconditions before execute

        :param facts:
        :return:
        """
        # self.pre_conditions must be contained into World.facts
        if self.pre_conditions <= facts:
            return True
        else:
            return False

    def change_facts(self):
        """ Every action must change the world facts. (STRIPS)
        :return:
        """
        pass


class Actions:

    def __init__(self):
        self.actions = list()

    def add_action(self, action: Action):
        self.actions.append(action)

    def remove_action(self, action: Action):
        self.actions.remove(action)

    def get(self):
        return self.actions.pop()

    def __str__(self):
        return 'Actions: {}'.format(self.actions)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.actions)

    def __len__(self):
        return len(self.actions)


if __name__ == '__main__':
    actions = Actions()
    actions.add_action(action=Action(
        name='create_vpc',
        pre_conditions=['vpc_doesnt_exist'],
        post_effects=['vpc_exist'],
        negative_effects=['raise_costs']
    ))
    actions.add_action(
        Action(
            name='create_vpn',
            pre_conditions=['vpc_exist'],
            post_effects=['vpn_exists'],
            negative_effects=['raise_costs']
        )
    )
    actions.add_action(
        Action(
            name='create_nat',
            pre_conditions=['vpc_exist'],
            post_effects=['nat_exist'],
            negative_effects=['raise_costs']
        )
    )
    actions.add_action(
        Action(
            name='create_asg',
            pre_conditions=['vpn_exist'],
            post_effects=['asg_exist'],
            negative_effects=['raise_costs']
        )
    )
    print(actions)
    change_resource = Action(
        name='change_resource',
        pre_conditions=['resource_exit'],
        post_effects=['resource_status_changed'],
        negative_effects=['resource_mutated']
    )
    actions.add_action(change_resource)
    print(actions)
    for action in actions:
        print(action)

