import subprocess
import inspect
import json
import boto3

from Goap.Errors import *


class AWSSensorResponse:
    """ SensorReturn is a class for represent the agent's sensor's return """

    def __init__(self, **kwargs):
        """

        :param kwargs: expects respose as dict argument and parse aws http response or shell Popen.response
        """
        self.return_code = None
        self.output = None
        self.error = None
        self.name = kwargs.get('name', None)
        self.sensor_response = kwargs.get('response', None)
        self._json_parsed_response = None

        self.__parse_aws_api_http_response()

    def __parse_aws_api_http_response(self):
        self._json_parsed_response = json.loads(self.sensor_response)
        self.return_code = self._json_parsed_response['ResponseMetadata']['HTTPStatusCode']
        if self.return_code == '200':
            self.output = self._json_parsed_response
        else:
            self.error = self._json_parsed_response

    def __repr__(self):
        json_data = {}
        if self.output:
            json_data = {'return_code': self.return_code, 'output': str(self.output)}
        elif self.error:
            json_data = {'return_code': self.return_code, 'error': str(self.error)}
        return json.dumps(json_data, skipkeys=True)

    def __str__(self):
        return self.__repr__()


class ShellSensorResponse:
    """ SensorReturn is a class for represent the agent's sensor's return """

    def __init__(self, **kwargs):
        """

        :param kwargs: return_code, output and error
        """
        self.name = kwargs.get('name', None)
        self.return_code = kwargs.get('return_code', None)
        self.output = kwargs.get('output', None)
        self.error = kwargs.get('error', None)

    def __return_message(self):
        if self.return_code == 0:
            return {'return_code': self.return_code, 'output': self.output}
        else:
            return {'return_code': self.return_code, 'error': self.error}

    def __repr__(self):
        return str(self.__return_message())

    def __str__(self):
        return self.__repr__()


class SensorResponse:

    def __init__(self, **kwargs):
        self.sensor_type = kwargs.get('type', None)
        self.sensor_response = self.__adapt_response(**kwargs)

    def __adapt_response(self, **kwargs):
        if self.sensor_type == 'shell':
            response = ShellSensorResponse(**kwargs)
        elif self.sensor_type == 'awsapi':
            response = AWSSensorResponse(**kwargs)
        else:
            raise '{} Need to specify the sensor\'s type'.format(SensorError)

        return response


class ShellSensor:
    """ Shell Sensor object factory

    """

    def __init__(self, name: str, shell: str=None):
        """ Sensor object

        :param name: Sensor's name
        :param shell: A string containing a shell command and its args
        :param obj: An class method that returns returncode, stdout and stderr
        """
        self.name = name
        self.type = 'shell'
        self.shell = shell
        self.return_code = None
        self.stdout = None
        self.stderr = None
        self.response = {}

    def __repr__(self):
        return 'Name: {}'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def __exec(self):
        """ Executes the sensor. Sensor's can be objects or a cli command

        :return SensorResponse:
        """
        cmd = self.shell
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        try:
            stdout, stderr = proc.communicate(timeout=30)
            returncode = proc.returncode
            self.response = ShellSensorResponse(name=self.name, output=stdout, error=stderr, return_code=returncode)
        except TimeoutError as e:
            proc.kill()
            raise('{}'.format(e))

        return self.response

    def __call__(self):
        return self.__exec()


class AWSRequestSensor:
    """ Sensor object factory

    """

    def __init__(self, name: str, obj: classmethod=None):
        """ Sensor object

        :param name: Sensor's name
        :param shell: A string containing a shell command and its args
        :param obj: An class method that returns returncode, stdout and stderr
        """
        self.name = name
        self.obj = obj
        self.return_code = None
        self.stdout = None
        self.stderr = None
        self.response = {}

    def __repr__(self):
        return 'Name: {}'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def __call_obj(self):
        """ Executes the sensor. Sensor's can be objects or a cli command

        :return SensorResponse:
        """
        if self.obj:
            self.response = self.obj()
        return AWSSensorResponse(name=self.name, response=self.response)

    def __call__(self):
        return self.__call_obj()


class Sensors:

    def __init__(self, sensors: list=[]):
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

    def add(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        if kwargs.get('shell') and kwargs.get('obj'):
            raise SensorMultipleTypeError

        name = kwargs.get('name')
        shell = kwargs.get('shell', None)
        obj = kwargs.get('obj', None)
        if shell:
            self.add_shell_sensor(name, shell)
        elif obj:
            self.add_obj_sensor(name, obj)

    def add_shell_sensor(self, name, shell):
        if not ShellSensor(name=name, shell=shell) in self.sensors:
            self.sensors.append(ShellSensor(name=name, shell=shell))
        else:
            raise SensorAlreadyInCollectionError

    def add_obj_sensor(self, name, obj):
        if not AWSRequestSensor(name=name, obj=obj) in self.sensors:
            self.sensors.append(AWSRequestSensor(name=name, obj=obj))
        else:
            raise SensorAlreadyInCollectionError

    def exec_all(self) -> list:
        responses = [s() for s in self.sensors]
        return responses


class AWSSensors:

    def __init__(self, tag: dict, sensor: str):
        """
        :self.values: it is a shared dictionary where the sensors stores the results of its inspections
        """
        self.values = {}
        self.ec2 = boto3.client('ec2', region_name='us-east-1')
        self.rds = boto3.client('rds', region_name='us-east-1')
        self.tag = tag
        self.sensor = sensor

    def __list_class_methods(self):
        return inspect.getmembers(self, predicate=inspect.ismethod)

    @staticmethod
    def __validate_aws_response(resource, response):

        if len(json.loads(response)[resource]) >= 1:
            return True
        else:
            return False

    def check_vpc_by_tag(self) -> AWSSensorResponse:
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        resource = 'Vpcs'
        key, value = self.tag.popitem()
        aws_response = self.ec2.describe_vpcs(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

        if self.__validate_aws_response(resource, aws_response):
            return_code, output, error = aws_response, None, 0
        else:
            return_code, output, error = 1, None, aws_response

        return SensorResponse(return_code, output, error)

    def run(self):
        try:
            obj = getattr(self, self.sensor)
            obj_response = obj()
            return obj_response
        except:
            raise SensorError


if __name__ == '__main__':
    # ACTIONS
    sensor_ec2_describe_by_tag = boto3.client('ec2')
    """
    sensors = Sensors()
    # VPC/Network set
    sensors.add_shell_sensor(
        name='ListFilesOnTMP',
        shell='ls -1 /tmp/'
    )
    sensors.add_shell_sensor(
        name='ListFilesOnPWD',
        shell='ls -1'
    )
    sensors.add_shell_sensor(
        name='ExecutesShell',
        shell='command_not_found.sh'
    )
    response = sensors.exec_all()
    print('responses: ', response)
    for r in response:
        print('response: ', r)
    """
    aws_sensors = Sensors()
    aws_sensors.add(
        name='VpcState',
        shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].State" --output text'
    )
    aws_sensors.add(
        name='VpcId',
        shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].VpcId" --output text'
    )
    resp_aws = aws_sensors.exec_all()
    print('responses: ', resp_aws)


