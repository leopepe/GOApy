from Goap.utils.os.ShellCommand import ShellCommand
from Goap.Action import Actions
from Goap.Sensor import Sensors
from Goap.Automaton import AutomatonController
from os.path import dirname


ACTIVE_NODES = '/tmp/tmp.actv_nds'
ACTIVE_HTTP_SRVS = '/tmp/tmp.actv_http'
SCANNED_HOSTS = '/tmp/scanned_hosts.txt'
PROJECT_DIR = dirname(__file__)


def setup_sensors() -> Sensors:
    """
    The sensors must: identify active nodes
                      identify http active listen hosts
                      identify http server app and version
    """
    list_active_nodes = ShellCommand(
        f"{PROJECT_DIR}/sensors/list_active_nodes.sh"
    )
    list_active_http_srvs = ShellCommand(
        f"{PROJECT_DIR}/sensors/list_active_http_servers.sh"
    )
    sensors = Sensors()
    sensors.add(
        name="list_active_nodes",
        binding="are_there_active_nodes",
        func=list_active_nodes
    )
    sensors.add(
        name="check_active_http_servers",
        binding="are_there_http_servers",
        func=list_active_http_srvs
    )
    return sensors


def setup_actions() -> Actions:
    """
    The actions must be able to allow: scan active nodes
                                       scan host for http vuln
                                       exploit vuln hosts
    """
    scan_http_vuln = ShellCommand(f"{PROJECT_DIR}/actions/scan_http_vuln.sh")
    actions = Actions()
    actions.add(
        name="scan_http_vuln",
        pre_conditions={"are_there_http_servers": "true", "checked_all_http_servers": "false"},
        effects={"checked_all_http_servers": "true"},
        func=scan_http_vuln,
        cost=0.2

    )
    return actions


if __name__ == "__main__":
    sensors = setup_sensors()
    actions = setup_actions()
    world_state = {
        "are_there_active_nodes": "false",
        "are_there_http_servers": "false",
        "checked_all_http_servers": "false"
    }
    automaton = AutomatonController(
        name="http_vulneratron",
        actions=actions,
        sensors=sensors,
        world_state=world_state
    )
    automaton.goal = {
        "checked_all_http_servers": "true"
    }
    # automaton.planner.graph.plot()
    automaton.start()
