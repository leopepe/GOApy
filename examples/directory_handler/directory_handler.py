from goap.utils.os.shell_command import ShellCommand
from goap.Action import Actions
from goap.Sensor import Sensors
from goap.Automaton import AutomatonController


def setup_sensors():
    sense_dir_state = ShellCommand(
        command='if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi'
    )
    sense_dir_content = ShellCommand(
        command='[ -f /tmp/goap_tmp/.token ] && echo -n "token_found" || echo -n "token_not_found"'
    )
    sensors = Sensors()
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
        conditions={
            'tmp_dir_state': 'not_exist',
            'tmp_dir_content': 'token_not_found'},
        effects={
            'tmp_dir_state': 'exist',
            'tmp_dir_content': 'token_not_found'},
        func=mkdir)
    actions.add(
        name='CreateToken',
        conditions={
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
