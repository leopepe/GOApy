import subprocess
import inspect
import json
import boto3


class SensorError(Exception):
    """ Sensor's Error base class """
    pass


class SensorResponse:
    """ SensorReturn is a class for represent the agent's sensor's return """

    def __init__(self, return_code, stdout: str=None, stderr: str=None):
        self.return_code = return_code
        self.output = stdout
        self.error = stderr

    def __repr__(self):
        args = [i for i in (self.output, self.error) if i]
        return 'return code: {}, output {}'.format(*args)


class Sensor:
    """ Sensor base class

    """

    def __init__(self, name: str, shell: str=None, obj: classmethod=None):
        self.name = name
        self.shell = shell
        self.obj = obj

    def __runner(self):
        # init response
        response = None

        if self.obj:
            # response = lambda: None
            response.return_code, response.stdout, response.stderr = self.obj()

        if self.shell:
            cmd = self.shell.split()
            response = subprocess.run(cmd, shell=True, check=True)

        return SensorResponse(return_code=response.returncode, stdout=response.stdout, stderr=response.stderr)

    def __call__(self):
        response = self.__runner()
        return response


class Sensors:

    def __init__(self, sensors: list=[]):
        self.sensors = sensors

    def __iter__(self):
        return iter(self.sensors)

    def __add__(self, sensor):
        if not isinstance(sensor, self):
            self.sensors.append(sensor)
        else:
            raise SensorError

    def __delete__(self, sensor):
        self.sensors.remove(sensor)

    def __repr__(self):
        return self.sensors

    def run_all(self):
        responses = [s.run() for s in self.sensors]
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

    def check_vpc_by_tag(self) -> SensorResponse:
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        resource = 'Vpcs'
        key, value = self.tag.popitem()
        response = self.ec2.describe_vpcs(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

        if self.__validate_aws_response(resource, response):
            return_code, output, error = response, None, 0
        else:
            return_code, output, error = 1, None, response

        return SensorResponse(return_code, output, error)

    def run(self):
        try:
            obj = getattr(self, self.sensor)
            response = obj()
            return response
        except:
            raise SensorError
