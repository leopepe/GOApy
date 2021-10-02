# Examples

In this section you can take a look on practical examples on how to use the GOAPy library and its engine to produce automatons.

## Directory Handler

Lets suppose that you need to ensure that a directory must exist and it needs an specific file inside of it. To accomplish that object you can create sensors that would monitor the directory and report changes on it.
Based on the state of the directory the automaton would  make the decision on which actions it need to do to guarantee the desired state of the directory.

### Code

```python
from goap.Action import Actions
from goap.Sensor import Sensors
from goap.Automaton import AutomatonController


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

The sensors will detect if the directory exists and if the file ***.token*** is inside of the directory.
In this example the sensors and the actions are simle Linux shell commands. Note that there is no conditional statement on the python code, the automaton engine perform all the measurements and asserts to identify the necessary actions to be taken.
