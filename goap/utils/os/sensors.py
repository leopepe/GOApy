# -*- coding: utf-8 -*-
"""
 sensors.py

"""
from os import listdir
from os.path import isdir, isfile, exists

from lvm2py import *

from goap.sensor import *

""" TODO:
detect files older than X days
detect files with different from pattern X
detect files with pattern X
detect files with extension .X
detect if volume above X% usage
detect if vg needs more disks
detect if container X is running
"""


class OSFilePath(Sensor):
    """
    OSFilePath
    """

    def __init__(self, binding: str, name: str, path: str):
        """

        :param binding:
        :param name:
        :param path:
        """
        self.path = path
        super(Sensor).__init__(binding=binding, name=name)

    def exists(self):
        """

        :return:
        """
        return exists(self.path)

    def is_dir(self):
        """

        :return:
        """
        if self.exists():
            return isdir(self.path)
        else:
            return False

    def is_file(self):
        """

        :return:
        """
        if self.exists():
            return isfile(self.path)
        else:
            return False

    def content(self):
        """

        :return:
        """
        if self.exists():
            return ''.join(str(i + '\n') for i in listdir(self.path))
        else:
            return 'not_exist'


class DirectoryExist(OSFilePath):
    """
    DirectoryExist
    """

    def __init__(self, binding: str, name: str, path: str):
        """

        :param binding:
        :param name:
        :param path:
        """
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def exec(self):
        """

        :return:
        """
        return self.is_dir()


class FileExist(OSFilePath):
    """
    FileExist
    """

    def __init__(self, binding: str, name: str, path: str):
        """

        :param binding:
        :param name:
        :param path:
        """
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def exec(self):
        """

        :return:
        """
        return self.is_file()


class FileIsOlderThan(OSFilePath):
    """
    FileIsOlderThan
    """

    def __init__(self, binding: str, name: str, path: str):
        """

        :param binding:
        :param name:
        :param path:
        """
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def is_older(self, days: str):
        """

        :param days:
        :return:
        """
        pass


class FileNamePattern(OSFilePath):
    """
    FileNamePattern
    """

    def __init__(self, binding: str, name: str, path: str):
        """

        :param binding:
        :param name:
        :param path:
        """
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def has_name_pattern(self):
        """

        :return:
        """
        pass


class FileHasExtension(OSFilePath):
    """
    FileHasExtension
    """

    def __init__(self, binding: str, name: str, path: str):
        """

        :param binding:
        :param name:
        :param path:
        """
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def has_extension(self, extension: str):
        """

        :param extension:
        :return:
        """
        pass


class LVM(Sensor):
    """
    LVM
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.lvm = LVM()
        self.binding = kwargs.get('binding', None)
        self.binding = kwargs.get('name', None)
        self.vg_name = kwargs.get('vg_name', None)
        self.lv_name = kwargs.get('lv_name', None)
        super(Sensor).__init__(binding=self.binding, name=self.name)

    def vg_exists(self):
        """

        :return:
        """
        try:
            if self.lvm.get_vg(self.vg_name):
                return 'exist'
            else:
                return 'not_exist'
        except LookupError as lookup_error_exception:
            raise '{}'.format(lookup_error_exception)

    def vg_size(self):
        """

        :return:
        """
        pass

    def vg_available_space(self):
        """

        :return:
        """
        pass

    def lv_exists(self):
        """

        :return:
        """
        pass

    def lv_size(self):
        """

        :return:
        """
        pass


class VGExists(LVM):
    """
    VGExists
    """

    def __init__(self, binding: str, vg_name: str):
        """

        :param binding:
        :param vg_name:
        """
        super(Sensor).__init__(binding=binding, vg_name=vg_name)

    def exec(self):
        """

        :return:
        """
        return self.vg_exists()


if __name__ == '__main__':
    """
    __name__
    """
    pass
