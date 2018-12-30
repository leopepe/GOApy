# -*- coding: utf-8 -*-
"""
 errors.py

"""
from __future__ import absolute_import
from __future__ import unicode_literals


class OperationFailedError(Exception):
    """OperationFailedError"""

    def __init__(self, reason):
        """
        Args:
            reason:
        """

class SensorError(Exception):
    """Sensor's Error base class"""
    pass


class SensorMultipleTypeError(SensorError):
    """Sensor can not be two type at once"""
    pass


class SensorDoesNotExistError(SensorError):
    """Sensor do not exist"""
    pass


class SensorAlreadyInCollectionError(SensorError):
    """Sensor do not exist"""
    pass


class PlanError(Exception):
    """Plan Error Exception"""
    pass


class PlanFailed(PlanError):
    """Plan Failed Exception"""
    pass


class ActionError(Exception):
    """Action's Error base class"""
    pass


class ActionMultipleTypeError(ActionError):
    """Action cannot be two types at once"""
    pass


class ActionAlreadyInCollectionError(ActionError):
    """Action Already In Collection"""
    pass
