from Goap.Action import Actions
from Goap.Sensor import Sensors
from Goap.Automaton import AutomatonController


def setup_sensors():
    sensors = Sensors()
    sensors.add(
        name='SenseGitRepo',
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
        name='CloneGitRepo',
        pre_conditions={},
        effects={},
        shell='mkdir -p /tmp/goap_tmp'
    )
    actions.add(
        name='BuildProject',
        pre_conditions={},
        effects={},
        shell='touch /tmp/goap_tmp/.token'
    )
    actions.add(
        name='NotifyBuild',
        pre_conditions={},
        effects={},
        shell='touch /tmp/goap_tmp/.token'
    )
    return actions


def setup_automaton():
    world_state_matrix = {
        "git_repo_updated": 'Unknown',
        "build_project": 'Unknown',
        "notify_build": 'Unknown',
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
