# GOAPy [![Build Status](https://travis-ci.com/leopepe/GOApy.svg?branch=v0.2.0)](https://travis-ci.com/leopepe/GOApy)

![GOAPy](docs/_static/rdaneelolivaw.jpg "Oh my god, it's full of stars!")

***Goal-Oriented Action Planning (GOAP) implementation in Python***

## Introduction

GOAP is a real-time planning algorithm for autonomous agents (AA).
AA are able to create an action planning based on a set of actions available to the AA. 

The Planner class searches for the correct set of actions from an initial state to it' goal. 
To perform the search the planner sets a graph using the possible world states as nodes and the available actions as edges of the graph. To search  for the shortest path it uses the A* algorithm.  

## Usage

### Using the Automaton class

From the Agent.py class perspective the usage and interaction should be:

```python
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)
priorities = AutomatonPriorities([
    {'vpc_state': 'available', 'db_state': 'available', 'app_state': 'running'}
])
world_state_matrix = {
    "vpc_state": 'Unknown',
    "db_state": 'Unknown',
    "app_state": 'Unknown',
}
goal = {
    "vpc_state": "available",
    "db_state": "available",
    "app_state": "running",
}
aws_actions = Actions()
aws_actions.add(
    name='CreateVPC',
    pre_conditions={'vpc_state': 'unavailable', 'db_state': 'unavailable', 'app_state': 'unavailable'},
    effects={'vpc_state': 'available', 'db_state': 'unavailable', 'app_state': 'unavailable'},
    shell='echo "vpc created"'
)
aws_actions.add(
    name='CreateDB',
    pre_conditions={'vpc_state': 'available', 'db_state': 'unavailable', 'app_state': 'unavailable'},
    effects={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'unavailable'},
    shell='echo "db created"'
)
aws_actions.add(
    name='CreateApp',
    pre_conditions={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'unavailable'},
    effects={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'running'},
    shell='echo "app created" > /tmp/CreateApp.out'
)
aws_sensors = Sensors()
aws_sensors.add(
    name='FindProjectVPC',
    # shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].State" --output text',
    shell='echo -n "unavailable"',
    binding='vpc_state'
)
aws_sensors.add(
    name='FindProjectDB',
    # shell='aws rds describe-db-instances --filters "Name=db-instance-id,Values=rds-oraculo" --query "DBInstances[].DBInstanceStatus" --output text',
    shell='echo -n "unavailable"',
    binding='db_state'
)
aws_sensors.add(
    name='CheckAppState',
    shell='echo -n "unavailable"',
    binding='app_state'
)
ai = Automaton(name='infra_builder', actions=aws_actions, sensors=aws_sensors, world_state=world_state_matrix)
# Control
# what is the environment status? what does the sensors return? ai has a goal?
# goal = priorities # object not working returning object rather then dict
ai.input_goal(goal)
ai.sense()
pp.pprint(
    'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(ai.world_state, ai.action_plan, ai.actions_response)
)
ai.plan()
ai.act()
pp.pprint(
    'Acknowledge world: {}, Action Plan: {}, Result: {}'.format(ai.world_state, ai.action_plan, ai.actions_response)
)
```

## Version

v0.2.0

