import subprocess
from typing import Callable

from Goap.Errors import SensorAlreadyInCollectionError, SensorDoesNotExistError


class Sensor:
    """ Sensor object factory """

    def __init__(self, name: str, binding: str, func: Callable):
        """ Sensor object model

        :param binding: string containing the key name
                        which the sensor will right to
        :param name: string containing the name of the sensor
        """
        self.binding = binding
        self.name = name
        self.func = func
        self.response = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__repr__()

    def __call__(self):
        return self.exec()

    def exec(self):
        try:
            stdout, stderr, return_code = self.func()
        except RuntimeError as e:
            raise RuntimeError(
                f"Error executing function {self.func}. Exception: {e}"
            )
        self.response = SensorResponse(
            stdout=stdout,
            stderr=stderr,
            return_code=return_code
        )
        return self.response


class SensorResponse:

    def __init__(
        self,
        stdout: str = '',
        stderr: str = '',
        return_code: int = 0,
    ):
        """

        :param name:
        :param sensor_type:
        """
        self._stdout = stdout
        self._stderr = stderr
        self.return_code = return_code

    def __str__(self):
        response = self.stdout
        if self.stderr:
            response = self.stderr
        return 'Response: {}, ReturnCode: {}'.format(response, self.return_code)

    def __repr__(self):
        return self.__str__()

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, value: str):
        self._stdout = value.rstrip('\r\n')

    @property
    def stderr(self):
        return self._stderr

    @stderr.setter
    def stderr(self, value: str):
        self._stderr = value.rstrip('\r\n')

    @property
    def response(self):
        if self.stdout:
            return self.stdout
        else:
            return self.stderr

    @response.setter
    def response(self, value):
        self.response = value


class Sensors:

    def __init__(self, sensors: list = []):
        """ Collection of sensors, adds only unique sensors

        :param sensors: List containing the sensor objects
        """
        self.sensors = sensors

    def __str__(self):
        names = [sensor.name for sensor in self.sensors]
        return '{}'.format(names)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        if self.sensors:
            return len(self.sensors)
        else:
            return 0

    def __iter__(self):
        return iter(self.sensors)

    def __delete__(self, sensor):
        if sensor in self.sensors:
            self.sensors.remove(sensor)
        else:
            raise SensorDoesNotExistError

    def __call__(self, name: str):
        """ Search for sensor, return None if does not match

        :param name: sensor's name
        :return: Sensor
        """
        sens = None
        for s in self.sensors:
            if s.name == name:
                sens = s
        return sens

    def get(self, name):
        result = None
        for sensor in self.sensors:
            if sensor.name == name:
                result = sensor
        return result

    def add(self, name: str, binding: str, func: Callable):
        if not self.get(name=name):
            self.sensors.append(Sensor(name=name, binding=binding, func=func))
        else:
            raise SensorAlreadyInCollectionError(
                f"Another sensor is using the same name: {name}"
            )

    def remove(self, name: str):
        result = False
        for sensor in self.sensors:
            if sensor.name == name:
                self.sensors.remove(sensor)
                result = True
        return result

    def exec_all(self) -> list:
        responses = [s.exec() for s in self.sensors]
        return responses
