# GOAPy 
[![Build Status](https://travis-ci.com/leopepe/GOApy.svg?branch=master)](https://travis-ci.com/leopepe/GOApy) [![Coverage Status](https://coveralls.io/repos/github/leopepe/GOApy/badge.svg?branch=master)](https://coveralls.io/github/leopepe/GOApy?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/41a49ddaaf54400d9dd3d08f7bb1852a)](https://www.codacy.com/manual/lpepefreitas/GOApy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=leopepe/GOApy&amp;utm_campaign=Badge_Grade) [![PyPI version](https://badge.fury.io/py/Goap.svg)](https://badge.fury.io/py/Goap) [![Python Formater](https://github.com/leopepe/GOApy/actions/workflows/autopep8.yml/badge.svg?branch=master)](https://github.com/leopepe/GOApy/actions/workflows/autopep8.yml)

**Version**: 0.3.0

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
from goap.utils.os.shell_command import ShellCommand
from goap.Action import Actions
from goap.Sensor import Sensors
from goap.Automaton import AutomatonController


def setup_sensors():
    """ The sensor collection can add any callable object to the collection 
        and call it returning the output to the binding key in the WorldState dictionary
    """
    sense_dir_state = ShellCommand(
        command='if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi'
    )
    sense_dir_content = ShellCommand(
        command='[ -f /tmp/goap_tmp/.token ] && echo -n "token_found" || echo -n "token_not_found"'
    )
    sensors = Sensors()
    # add a shell sensor that will check if a directory exist and returns a string with
    # "exists" or "not_exist"
    # The return string will update the automaton's world state
    sensors.add(
        name='SenseTmpDirState',
        func=sense_dir_state,
        binding='tmp_dir_state')
    sensors.add(
        name='SenseTmpDirContent',
        func=sense_dir_content,
        binding='tmp_dir_content')
    return sensors


def setup_actions():
    mkdir = ShellCommand(
        command='mkdir -p /tmp/goap_tmp'
    )
    mktoken = ShellCommand(
        command='touch /tmp/goap_tmp/.token'
    )
    actions = Actions()
    actions.add(
        name='CreateTmpDir',
        pre_conditions={
            'tmp_dir_state': 'not_exist',
            'tmp_dir_content': 'token_not_found'},
        effects={
            'tmp_dir_state': 'exist',
            'tmp_dir_content': 'token_not_found'},
        func=mkdir)
    actions.add(
        name='CreateToken',
        pre_conditions={
            'tmp_dir_state': 'exist',
            'tmp_dir_content': 'token_not_found'},
        effects={
            'tmp_dir_state': 'exist',
            'tmp_dir_content': 'token_found'},
        func=mktoken)
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

