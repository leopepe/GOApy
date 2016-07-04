from collections import deque
from World import World
from Actions import Actions


class Plan:

    def __init__(self):
        self.steps = deque()

    def put(self, action):
        self.steps.append(action)

    def get(self, action):
        self.steps.pop(action)

    def empty(self):
        return len(self.steps) == 0

    def __str__(self):
        return 'Plan: <object>, Steps: {0}, Total: {1}'.format(self.steps, len(self.steps))

    def __repr__(self):
        return self.__str__()


class Planner:

    def __init__(self, actions: list, world: World, goal: str):
        self.actions = actions
        self.world = world
        self.plan = Plan()
        self.goal = goal

    def get_facts(self):
        return self.world

    def get_actions(self):
        return self.actions

    def satisfy_goal(self):
        if self.goal in self.world.facts:
            return True
        else:
            return False

    def breadth_first_search(self):
        # plan = self.plan
        while len(self.actions) != 0:

            if self.satisfy_goal():
                break

            for action in actions:
                if action.satisfy_preconditions(self.world.facts):
                    self.world.facts.extend(action.post_effects)
                    self.plan.put(self.actions.get())

        return self.plan


if __name__ == '__main__':

    from Actions import Action
    from World import World

    world = World(facts=['vpc_doesnt_exist'])
    goal = 'win'
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
    planner = Planner(actions=actions, world=world, goal='asg_exist')
    print(planner.breadth_first_search())
