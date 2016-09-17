from Goap.Action import Action
from Goap.World import World
from Goap.Planner import Planner

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