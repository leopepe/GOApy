from Goap import Sensor
from typing import Optional, Tuple
from Goap.Action import Action
import subprocess


class ShellCommand(object):
    """ Creates an callable object  """

    def __init__(self, command: str, timeout: int = 30):
        self.command = command
        self.timeout = timeout
        self.response = None

    def __call__(self):
        self.run(self.command)

    def run(self, command=Optional[str]) -> Tuple[str, str, int]:
        process = subprocess.Popen(
            ['/bin/sh', '-c', command],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        try:
            stdout, stderr = process.communicate(timeout=self.timeout)
            return_code = process.returncode
            self.response = (stdout, stderr, return_code)
        except RuntimeError as e:
            raise Exception(
                f'Error opening process {self.command}: {e}')
        finally:
            process.kill()

        return self.response
