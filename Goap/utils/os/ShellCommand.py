from typing import Optional, Tuple
from subprocess import Popen, PIPE


class ShellCommand(object):
    """ Creates an callable object which executes a shell command """

    def __init__(self, command: str, timeout: int = 30):
        self.command = command
        self.timeout = timeout
        self.response = None

    def __call__(self):
        return self.run(self.command)

    def run(self, command=Optional[str]) -> Tuple[str, str, int]:
        process = Popen(
            ['/bin/sh', '-c', command],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
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
