from __future__ import absolute_import
from __future__ import unicode_literals


class OperationFailedError(Exception):
    def __init__(self, reason):
        self.msg = reason


class SensorError(Exception):
    """ Sensor's Error base class """
    pass


class SensorMultipleTypeError(SensorError):
    """ Sensor can not be two type at once """
    pass


class SensorDoesNotExistError(SensorError):
    """ Sensor do not exist """
    pass


class SensorAlreadyInCollectionError(SensorError):
    """ Sensor do not exist """
    pass


class PlanError(Exception):
    pass


class PlanFailed(PlanError):
    pass