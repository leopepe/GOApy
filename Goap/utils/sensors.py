import boto3


class AWSClient:
    def __init__(self, client: str, filters: list=[], tag: dict={}):
        self.filters = filters
        self.tag = tag
        self.client = boto3.client(client)
        if self.tag != {}:
            self.filters = self.__dict_into_filter(tag)

    @staticmethod
    def __dict_into_filter(tag: dict):
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
            raise('{}'.format(e))

    def __get_item(self, key):
        vpcs = self.__desc()
        return [vpc[key] for vpc in vpcs].pop()

    def exec(self):
        pass


class VPCClient(AWSClient):

    def __init__(self):
        super().__init__(client='ec2')

    def __desc(self):
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
    pass

