# GOAPy

![GOAPy](/docs/rdaneelolivaw.jpg "Oh my god, it's full of stars!")

***G***oal-***O***riented ***A***ction ***P***lanning (GOAP) implementation in ***Py***thon

## Introduction

GOAP is a real-time planning algorithm for autonomous agents (AA).
AA are able to create an action plan based on a set of actions available to the AA. 

The Planner class searches for the correct set of actions from an initial state to it' goal. 
To perform the search the planner sets a graph using the possible world states as nodes and the available actions as edges of the graph. To search  for the shortest path it uses the A* algorithm.  

## Usage

### Using the Agent class

From the Agent.py class perspective the usage and interaction should be:

```python
from Goap.Action import Actions
import pprint

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
init_state = {'vpc': False, 'app': False, 'db': False}
init_goal = {'vpc': True, 'db': True, 'app': True}
ai_cloud_builder = Agent(name='CloudBuilder', state=init_state, goal=init_goal, actions=actions)
result = ai_cloud_builder.start()
pprint.pprint(result, indent=2, width=80)
```

## Version
