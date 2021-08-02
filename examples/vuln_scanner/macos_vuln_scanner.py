from Goap.utils.os.ShellCommand import ShellCommand
from Goap.Action import Actions
from Goap.Sensor import Sensors
from Goap.Automaton import AutomatonController


TARGET_FILE_PATH = '/tmp/target_hosts.txt'
SCANNED_HOSTS = '/tmp/scanned_hosts.txt'


def setup_sensors() -> Sensors:
    """
    The sensors must: identify active nodes
                      identify http active listen hosts
                      identify http server app and version
    """
    default_inet = ShellCommand("netstat -nr -f inet|grep default|tr -s ' '|cut -d ' ' -f 4")
    default_gw = ShellCommand("netstat -nr -f inet|grep default|tr -s ' '|cut -d ' ' -f 2")
    list_active_nodes = ShellCommand(
        "nmap -T5 -sn 192.168.0.0/24|grep 'Host is up' -B 1|grep 'scan report'|awk '{print $NF}'|sed 's/(//g'|sed 's/)//g > {TARGET_FILE_PATH}'"
    )
    # check if there are new nodes in list_active_nodes file
    # if there are new nodes write it to nodes_to_scan
    is_there_new_active_nodes = ShellCommand(f"diff {TARGET_FILE_PATH} {SCANNED_HOSTS}")
    sensors = Sensors()
    sensors.add(
        name="default_inet",
        binding="net_default_interface",
        func=default_inet
    )
    sensors.add(
        name="default_gw",
        binding="net_default_gateway",
        func=default_gw
    )
    sensors.add(
        name="active_nodes",
        binding="network_active_nodes",
        func=list_active_nodes
    )
    sensors.add(
        name="is_there_new_active_nodes",
        binding="there_is_new_nodes",
        func=is_there_new_active_nodes
    )
    return sensors


def setup_actions() -> Actions:
    """
    The actions must be able to allow: scan active nodes
                                       scan host for http vuln
                                       exploit vuln hosts
    """
    scan_http_hosts = ShellCommand(f"nmap -Pn -T5 -p 80 -sS -sV --version-all -iL {TARGET_FILE_PATH}")
    actions = Actions()
    actions.add(
        name="scan_http_hosts",
        pre_conditions={},
        effects={},
        func=scan_http_hosts,
        cost=0.2

    )
    return actions
