import subprocess

from goap.errors import SensorMultipleTypeError, \
    SensorAlreadyInCollectionError, SensorDoesNotExistError


class Sensor:
    """ Sensor object factory """

    def __init__(self, binding: str, name: str):
        """ Sensor object model

        :param binding: string containing the key name
        which the sensor will right to
        :param name: string containing the name of the sensor
        """
        self.binding = binding
        self.name = name
        self.response = {}

    def __repr__(self):
        return 'Name: {}'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def __call__(self, **kwargs):
        self.__init__(kwargs.get('binding'), kwargs.get('name'))
        self.exec()

    def exec(self):
        """ Interface method to the sensors execution """
        pass


class SensorResponse:

    def __init__(self, name: str, sensor_type: str, return_code: str,
                 stdout: str = '', stderr: str = ''):
        """

        :param name:
        :param sensor_type:
        """
        self.name = name
        self.sensor_type = sensor_type
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.__response_parser()

    def __str__(self):
        result = f'Name: {self.name}, ' \
            f'Response: {self.response}, ' \
            f'ReturnCode: {self.return_code}'
        return result

    def __repr__(self):
        return self.__str__()

    def __response_parser(self):
        if not self.stdout == '':
            self.response = self.stdout
        elif not self.stderr == '':
            self.response = self.stderr


class ShellSensor(Sensor):
    """ Shell Sensor object factory """

    def __init__(self, binding: str, name: str, shell: str = None):
        self.response = None
        self.type = 'shell'
        self.shell = shell
        Sensor.__init__(self, binding=binding, name=name)

    def exec(self) -> SensorResponse:
        cmd = self.shell
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        try:
            stdout, stderr = process.communicate(timeout=30)
            return_code = process.returncode
            self.response = SensorResponse(
                name=self.name,
                sensor_type='shell',
                stdout=stdout,
                stderr=stderr,
                return_code=return_code
            )
        except TimeoutError as e:
            process.kill()
            raise ('{}'.format(e))
        finally:
            process.kill()

        return self.response


class Sensors:

    def __init__(self, sensors: list = []):
        """ Collection of sensors, adds only unique sensors

        :param sensors: List containing the sensor objects
        """
        self.sensors = sensors

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

    def __repr__(self):
        output = []
        for s in self.sensors:
            output.append(s.__repr__())
        return str(output)

    def get(self, name):
        result = None
        for sensor in self.sensors:
            if sensor.name == name:
                result = sensor
        return result

    def __add_shell_sensor(self, name, shell, binding):
        if not ShellSensor(name=name,
                           shell=shell,
                           binding=binding) in self.sensors:
            self.sensors.append(ShellSensor(name=name,
                                            shell=shell,
                                            binding=binding))
        else:
            raise SensorAlreadyInCollectionError

    def __add_obj_sensor(self, name, obj, binding):
        raise NotImplementedError

    def add(self, **kwargs):
        if kwargs.get('shell') and kwargs.get('obj'):
            raise SensorMultipleTypeError

        name = kwargs.get('name')
        shell = kwargs.get('shell', None)
        obj = kwargs.get('obj', None)
        binding = kwargs.get('binding', None)
        if shell:
            self.__add_shell_sensor(name, shell, binding)
        elif obj:
            self.__add_obj_sensor(name, obj, binding)

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


if __name__ == '__main__':
    # ACTIONS
    '''
    aws_sensors = Sensors()
    aws_sensors.add(
        name='VpcState',
        shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name",
        "Name=tag-value,Values=vpc_plataformas_stg"
        --query "Vpcs[].State" --output text'
    )
    aws_sensors.add(
        name='VpcId',
        shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name",
        "Name=tag-value,Values=vpc_plataformas_stg"
        --query "Vpcs[].VpcId" --output text'
    )
    # resp_aws = aws_sensors.exec_all()
    # print('responses: ', resp_aws)
    #
    '''
    fs_sensors = Sensors()
    fs_sensors.add(
        name='FindOldFilesOnTmp',
        shell='find /tmp/log_tests -mtime +1|wc -l|xargs test -f && '
              'echo "Exists" || echo "None"',
        binding='old_files'
    )
    fs_sensors.add(
        name='LogFilesToCompact',
        shell='test $(find /tmp/log_tests -name "*.log" '
              '-type f -size +900M| wc -l) -gt 0 && echo "Exists" '
              '|| echo "None"',
        binding='old_files'
    )
    resp = fs_sensors.exec_all()
    print('responses for fs sensors: {}', resp)
