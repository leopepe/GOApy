class World:

    def __init__(self, facts: list):
        """ The world ins the environment for the agents to interact.
            The facts are constantly updated by the agent' actions

        :param facts:
        :return:
        """
        self.facts = facts

    def add_fact(self, fact: str):
        """ Include a world fact

        :param fact:
        :return:
        """
        self.facts.append(fact)

    def remove_fact(self, fact: str):
        """ Remove a world fact

        :param fact:
        :return:
        """
        self.facts.remove(fact)

    def clear_facts(self):
        """ Clear all world facts

        :return:
        """
        self.facts.clear()

    def get_facts(self):
        """ Return all world's facts

        :return: self.facts
        """
        return self.facts


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


