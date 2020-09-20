from Goap import Sensor
from typing import Optional, Tuple
from Goap.Action import Action
import subprocess


class ShellCommand(object):
    """ Creates an callable object  """

    def __init__(self, command: str):
        self.command = command
        self.response = None

    def __call__(self):
        self.exec(self.command)

    def exec(self, command=Optional[str]) -> Tuple[str, str, int]:
        process = subprocess.Popen(
            ['/bin/sh', '-c', command],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        try:
            stdout, stderr = process.communicate(timeout=30)
            return_code = process.returncode
            self.response = (stdout, stderr, return_code)
        except RuntimeError as e:
            raise(f'Error opening process {self.cmd}: {e}')
        finally:
            process.kill()

        return self.response


class ShellCommandSensor(Sensor):
    def __init__(self) -> None:
        pass


class ShellCommandAction(Action):
    def __init__(self) -> None:
        pass
