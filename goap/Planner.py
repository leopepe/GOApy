from World import Actions
from World import World

from collections import deque
import heapq


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
        return '{0}, NSteps: {1}, Steps: {2}'.format(self.__class__, len(self.steps), self.steps)

    def __repr__(self):
        return self.__str__()


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Planner:

    def __init__(self, actions: list, world: World, goal: list):
        self.actions = actions
        self.world = world
        self.plan = Plan()
        self.goal = goal
        # self.breadth_first_search()

    def get_facts(self):
        return self.world

    def get_actions(self):
        return self.actions

    def satisfy_goal(self):
        g = set(self.goal)
        f = set(self.world.facts)
        if g.issubset(f):
            return True
        else:
            return False

    # NOT WORKING PROPERLY
    def breadth_first_search(self):
        # plan = self.plan
        while len(self.actions) != 0:

            if self.satisfy_goal():
                break

            for action in actions:
                if action.satisfy_preconditions(self.world.get_facts()):
                    # self.world.add_fact(action.effects)
                    [self.world.add_fact(eff) for eff in action.effects]
                    # [self.world.remove_fact(neff) for neff in action.neg_effects]
                    self.plan.put(self.actions.get())

        return self.plan

    def a_star_search(self, start, goal):

        def __heuristics(preconds, facts):
            if preconds <= facts:
                return True

        visited = []
        cost = 0
        while len(actions) != 0:
            current = self.actions.get()

            if self.satisfy_goal():
                break

            if current <= visited:
                continue

            for facts in self.world.facts:
                if __heuristics(current.pre_conds, facts):
                    self.plan.put(current)
                    visited.append(current)

            cost += 1


if __name__ == '__main__':
    from World import Action
    from World import World

    # facts = {'VPC': False, 'VPN': False, 'NAT': False, 'ASG': False}
    facts = ['no_vpc', 'no_vpn', 'no_nat', 'no_asg']
    world = World(facts=facts)
    goal = ['asg_exist']
    actions = Actions()
    actions.add_action(action=Action(
        name='create_vpc',
        pre_conditions=['no_vpc'],
        post_effects=['vpc_exist'],
        negative_effects=['no_vpc']
    ))
    actions.add_action(
        Action(
            name='create_vpn',
            pre_conditions=['vpc_exist'],
            post_effects=['vpn_exists'],
            negative_effects=['no_vpn']
        )
    )
    actions.add_action(
        Action(
            name='create_nat',
            pre_conditions=['vpc_exist'],
            post_effects=['nat_exist'],
            negative_effects=['no_nat']
        )
    )
    actions.add_action(
        Action(
            name='create_asg',
            pre_conditions=['vpn_exist'],
            post_effects=['asg_exist'],
            negative_effects=['no_asg']
        )
    )
    actions.add_action(
        Action(
            name='create_instance',
            pre_conditions=['vpc_exist', 'vpn_exist'],
            post_effects=['instance_exist'],
            negative_effects=['raise_costs']
        )
    )
    actions.add_action(
        Action(
            name='destroy_vpn',
            pre_conditions=['no_nat', 'no_asg'],
            post_effects=['no_vpn'],
            negative_effects=['no_vpn']
        )
    )

    print('TestCase 1')
    planner = Planner(actions=actions, world=world, goal=goal)
    plan = planner.breadth_first_search()
    print(planner.plan)
    print(world.facts)
    print(planner.world.facts)
    """

    print('TestCase 2')
    plan = Planner(actions=actions, world=world, goal=goal).astar()
    print(planner.plan)
    print(world.facts)
    print(planner.world.facts)
    """