# -*- coding: utf-8 -*-
"""
 sensors.py

"""

import boto3


class AWSClient:
    """
    AWSClient
    """

    def __init__(self, client: str, filters: list = [], tag: dict = {}):
        """

        :param client:
        :param filters:
        :param tag:
        """
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
        """

        :param key:
        :return:
        """

    def exec(self):
        """

        :return:
        """


class EC2Client(AWSClient):
    """
    EC2Client
    """

    def __init__(self):
        """
        __init__
        """
        super().__init__(client='ec2')

    def __desc(self):
        """

        :return:
        """
        try:
            response = self.client.describe_instances(Filters=self.filters)
            return response
        except IOError as io_error_exception:
            raise ('{}'.format(io_error_exception))

    def __get_item(self, key):
        """

        :param key:
        :return:
        """
        vpcs = self.__desc()
        return [vpc[key] for vpc in vpcs].pop()

    def exec(self):
        """

        :return:
        """


class VPCClient(AWSClient):
    """
    VPCClient
    """

    def __init__(self):
        """
        __init__
        """
        super().__init__(client='ec2')

    def __desc(self):
        """ describe vpcs

        :return: AWS API Response
        :rtype: json
        """
        try:
            response = self.client.describe_vpcs(Filters=self.filters)
            return response
        except IOError as io_error_exception:
            raise ('{}'.format(io_error_exception))

    def __get_item(self, key):
        """

        :param key:
        :return:
        """
        vpcs = self.__desc()
        return [vpc[key] for vpc in vpcs].pop()

    def exec(self):
        """

        :return:
        """


class AWSCheckVPCUnique(VPCClient):
    """
    AWSCheckVPCUnique
    """

    def is_unique(self):
        """

        :return:
        """
        vpcs = self.__desc()
        if len(vpcs) >= 2:
            return False
        else:
            return True

    def exec(self):
        """

        :return:
        """
        return self.is_unique()


class AWSCheckVPCStatus(VPCClient):
    """
    AWSCheckVPCStatus
    """

    def status(self):
        """

        :return:
        """
        return self.__get_item(key='State')

    def exec(self):
        """

        :return:
        """
        return self.status()


class AWSCheckVPCIsDefault(VPCClient):
    """
    AWSCheckVPCIsDefault
    """

    def is_default(self):
        """

        :return:
        """
        return self.__get_item(key='IsDefault')

    def exec(self):
        """

        :return:
        """
        return self.is_default()


class AWSCheckInstancesCapacity(EC2Client):
    """
    AWSCheckInstancesCapacity
    """

    def __instances_cpu_utilization(self, instance_id: str):
        """

        :param instance_id:
        :return:
        """

    def exec(self):
        """

        :return:
        """


class AWSCheckLatestProjectAMI(EC2Client):
    """
    AWSCheckLatestProjectAMI
    """

    def __last_project_ami(self, version):
        """

        :param version:
        :return:
        """

    def exec(self):
        """

        :return:
        """


class AWSCheckInstancesWithOldAMI(EC2Client):
    """
    AWSCheckInstancesWithOldAMI
    """

    def __instances_with_old_ami(self):
        """

        :return: list of instances ids with AMI with an old version
        """


class AWSCheckOrphanEBS(EC2Client):
    """
    AWSCheckOrphanEBS
    """
