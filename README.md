# GOAPy [![Build Status](https://travis-ci.com/leopepe/GOApy.svg?branch=v0.2.0)](https://travis-ci.com/leopepe/GOApy) [![Coverage Status](https://coveralls.io/repos/github/leopepe/GOApy/badge.svg?branch=master)](https://coveralls.io/github/leopepe/GOApy?branch=v0.2.0)

![GOAPy](docs/_static/rdaneelolivaw.jpg "Oh my god, it's full of stars!")

***Goal-Oriented Action Planning (GOAP) implementation in Python***

## Introduction

GOAP is a real-time planning algorithm for autonomous agents (AA).
AA are able to create an action planning based on a set of actions available to the AA. 

The Planner class searches for the correct set of actions from an initial state to it' goal. 
To perform the search the planner sets a graph using the possible world states as nodes and the available actions as edges of the graph. To search  for the shortest path it uses the A* algorithm.  

## Usage

### Using the AutomatonController class

From the AutomatonController class perspective the usage and interaction should be:

```python
from Goap.Action import Actions
from Goap.Sensor import Sensors
from Goap.Automaton import AutomatonController


def setup_sensors():
    sensors = Sensors()
    sensors.add(
        name='SenseTmpDirState',
        shell='if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi',
        binding='tmp_dir_state'
    )
    sensors.add(
        name='SenseTmpDirContent',
        shell='[ -f /tmp/goap_tmp/.token ] && echo -n "token_found" || echo -n "token_not_found"',
        binding='tmp_dir_content'
    )
    return sensors


def setup_actions():
    actions = Actions()
    actions.add(
        name='CreateTmpDir',
        pre_conditions={'tmp_dir_state': 'not_exist', 'tmp_dir_content': 'token_not_found'},
        effects={'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'},
        shell='mkdir -p /tmp/goap_tmp'
    )
    actions.add(
        name='CreateToken',
        pre_conditions={'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_not_found'},
        effects={'tmp_dir_state': 'exist', 'tmp_dir_content': 'token_found'},
        shell='touch /tmp/goap_tmp/.token'
    )
    return actions


def setup_automaton():
    world_state_matrix = {
        "tmp_dir_state": 'Unknown',
        "tmp_dir_content": 'Unknown',
    }
    automaton = AutomatonController(
        name='directory_watcher',
        actions=setup_actions(),
        sensors=setup_sensors(),
        world_state=world_state_matrix
    )
    return automaton


def main():
    goal = {
        "tmp_dir_state": "exist",
        "tmp_dir_content": "token_found",
    }
    dir_handler = setup_automaton()
    dir_handler.goal = goal
    dir_handler.start()


if __name__ == '__main__':
    main()
```

## Version

v0.2.0

