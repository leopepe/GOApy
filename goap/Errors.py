from __future__ import absolute_import
from __future__ import unicode_literals


class OperationFailedError(Exception):
    def __init__(self, reason):
        self.msg = reason


class SensorError(Exception):
    """ Sensor's Error base class """


class SensorMultipleTypeError(SensorError):
    """ Sensor can not be two type at once """


class SensorDoesNotExistError(SensorError):
    """ Sensor do not exist """


class SensorAlreadyInCollectionError(SensorError):
    """ Sensor do not exist """


class PlanError(Exception):
    """ Generic plan error """


class PlanFailed(PlanError):
    """ Failed to produce a plan """


class ActionError(Exception):
    """ Action's Error base class """


class ActionMultipleTypeError(ActionError):
    """ Action cannot be two types at once """


class ActionAlreadyInCollectionError(ActionError):
    """ Action with same name already in collection """
