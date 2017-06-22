import subprocess
import boto3


class SensorResponse:
    """
    SensorReturn is a class for represent the agent's sensor's return

    """

    def __init__(self, return_code, stdout: str=None, stderr: str=None):
        self.return_code = return_code
        self.output = stdout
        self.error = stderr

    def __repr__(self):
        args = [i for i in (self.output, self.error) if i]
        return 'return code: {}, output {}'.format(*args)


class Sensor:
    """

    """

    def __init__(self, name: str, shell: str=None, obj: classmethod=None):
        self.name = name
        self.shell = shell
        self.obj = obj

    def __runner(self):
        response = None

        if self.obj:
            response = self.obj()

        if self.shell:
            cmd = self.shell.split()
            response = subprocess.run(cmd, shell=True, check=True)

        return SensorResponse(return_code=response.returncode, stdout=response.stdout, stderr=response.stderr)

    def run(self):
        response = self.__runner()
        return response


class Sensors:

    def __init__(self):
        self.sensors = list()

    def __iter__(self):
        return iter(self.sensors)

    def add(self, sensor: Sensor):
        self.sensors.append(sensor)

    def remove(self, sensor):
        self.sensors.remove(sensor)

    def run_all(self):
        responses = [s.run() for s in self.sensors]
        return responses


class SensorsAWS:

    def __init__(self, project_name: str):
        """
        :self.values: it is a shared dictionary where the sensors stores the results of its inspections
        """
        self.values = {}
        self.ec2 = boto3.client('ec2', region_name='us-west-2')
        self.rds = boto3.client('rds', region_name='us-west-2')
        self.tag = {'project': project_name}

    @classmethod
    def check_vpc_by_tag(cls):
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        ec2 = boto3.client('ec2', region_name='us-east-1')
        key, value = cls.tag.popitem()
        return ec2.describe_vpcs(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

    def check_aws_rds(self, tag: dict):
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        key = None
        value = None
        if len(tag) == 1:
            key, value = tag.popitem()

        if key and value:
            resp = self.ec2.describe_db_instances(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

            if len(resp['DBInstances']) == 1:
                return True
            elif len(resp['DBInstances']) > 1:
                return 'ERROR'
            elif len(resp['DBInstances']) == 0:
                return False

    def check_aws_instances(self, tag: dict):
        """ check if aws resource exists

        :param tag: {'project': 'project_name'}
        :return:
        """
        key = None
        value = None
        if len(tag) == 1:
            key, value = tag.popitem()

        if key and value:
            resp = self.ec2.describe_instances(Filters=[{'Name': 'tag:' + key, 'Values': [value]}])

            if len(resp['Instances']) == 1:
                return True
            elif len(resp['Instances']) > 1:
                return 'ERROR'
            elif len(resp['Instances']) == 0:
                return False

    def check_local_command_output(self, command: str=None):
        """ executes a command on the local system and expects status code 0 success.

        :param command
        :return:
        """
        # values = {}
        # self.values.update(values)
        pass

    def check_mock_module_vpc(self):
        val = choice([{'vpc': True}, {'vpc': False}])
        self.values.update(val)
        return True

    def check_mock_module_app(self):
        val = choice([{'app': True}, {'app': False}])
        self.values.update(val)
        return True

    def check_mock_module_db(self) -> bool:
        val = choice([{'db': True}, {'db': False}])
        # self.values with the result of the sensor inspections
        self.values.update(val)
        return True

    def run_all(self):
        case1 = {'vpc': False, 'db': False, 'app': False}

        case2 = {'vpc': True, 'db': True, 'app': False}

        case3 = {'vpc': True, 'db': False, 'app': False}

        case4 = {'vpc': True, 'db': 'inconsistent', 'app': True}

        case5 = {'vpc': True, 'db': True, 'app': 'unhealthy'}

        case6 = {'vpc': True, 'db': True, 'app': 'out_of_capacity'}

        cases = [case1, case2, case3, case4, case5, case6]
        case = choice(cases)
        self.values.update(case)
        return case
