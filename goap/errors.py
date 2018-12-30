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
        super().__init__(message=reason)


class SensorError(Exception):
    """Sensor's Error base class"""


class SensorMultipleTypeError(SensorError):
    """Sensor can not be two type at once"""


class SensorDoesNotExistError(SensorError):
    """Sensor do not exist"""


class SensorAlreadyInCollectionError(SensorError):
    """Sensor do not exist"""


class PlanError(Exception):
    """Plan Error Exception"""


class PlanFailed(PlanError):
    """Plan Failed Exception"""


class ActionError(Exception):
    """Action's Error base class"""


class ActionMultipleTypeError(ActionError):
    """Action cannot be two types at once"""


class ActionAlreadyInCollectionError(ActionError):
    """Action Already In Collection"""
