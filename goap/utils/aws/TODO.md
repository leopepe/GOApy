# TODO

* create clients and tests

```python
import boto3


class AWSClient:
    def __init__(self, client: str, filters: list = [], tag: dict = {}):
        self.filters = filters
        self.tag = tag
        self.client = boto3.client(client)
        if self.tag != {}:
            self.filters = self.__dict_into_filter(tag)

    @staticmethod
    def __dict_into_filter(tag: dict):
        """

        :param tag: Key / Value pair dict type
        :return: An AWS Filter format [{'Name': filter-name, 'Values': [val1, val2, ...]]
        """
        key = 'tag:{key}'.format(key=[*tag.keys()].pop())
        val = [*tag.values()].pop()
        return [{'Name': key, 'Values': [val]}]

    def __get_item(self, key):
        pass

    def exec(self):
        pass


class EC2Client(AWSClient):

    def __init__(self):
        super().__init__(client='ec2')

    def __desc(self):
        try:
            response = self.client.describe_instances(Filters=self.filters)
            return response
        except IOError as e:
            raise IOError(f'{e}')

    def __get_item(self, key):
        vpcs = self.__desc()
        return [vpc[key] for vpc in vpcs].pop()

    def exec(self):
        pass


class VPCClient(AWSClient):

    def __init__(self):
        super().__init__(client='ec2')

    def __desc(self):
        """ describe vpcs

        :return: AWS API Response
        :rtype: json
        """
        try:
            response = self.client.describe_vpcs(Filters=self.filters)
            return response
        except IOError as e:
            raise('{}'.format(e))

    def __get_item(self, key):
        vpcs = self.__desc()
        return [vpc[key] for vpc in vpcs].pop()

    def exec(self):
        pass


class AWSCheckVPCUnique(VPCClient):

    def is_unique(self):
        vpcs = self.__desc()
        if len(vpcs) >= 2:
            return False
        else:
            return True

    def exec(self):
        return self.is_unique()


class AWSCheckVPCStatus(VPCClient):

    def status(self):
        return self.__get_item(key='State')

    def exec(self):
        return self.status()


class AWSCheckVPCIsDefault(VPCClient):

    def is_default(self):
        return self.__get_item(key='IsDefault')

    def exec(self):
        return self.is_default()


class AWSCheckInstancesCapacity(EC2Client):

    def __instances_cpu_utilization(self, instance_id: str):
        pass

    def exec(self):
        pass


class AWSCheckLatestProjectAMI(EC2Client):

    def __last_project_ami(self, version):
        pass

    def exec(self):
        pass


class AWSCheckInstancesWithOldAMI(EC2Client):

    def __instances_with_old_ami(self):
        """

        :return: list of instances ids with AMI with an old version
        """


class AWSCheckOrphanEBS(EC2Client):
    pass

```
