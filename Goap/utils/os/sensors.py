from os import listdir
from os.path import isdir, isfile, exists

from Goap.Sensor import *


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

    def __init__(self, binding: str, name: str, path: str):
        self.path = path
        super(Sensor).__init__(binding=binding, name=name)

    def exists(self):
        return exists(self.path)

    def is_dir(self):
        if self.exists():
            return isdir(self.path)
        else:
            return False

    def is_file(self):
        if self.exists():
            return isfile(self.path)
        else:
            return False

    def content(self):
        if self.exists():
            return ''.join(str(i + '\n') for i in listdir(self.path))
        else:
            return 'not_exist'


class DirectoryExist(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def exec(self):
        return self.is_dir()


class FileExist(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def exec(self):
        return self.is_file()


class FileIsOlderThan(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def is_older(self, days: str):
        pass


class FileNamePattern(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def has_name_pattern(self):
        pass


class FileHasExtension(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super(Sensor).__init__(binding=binding, name=name, path=path)

    def has_extension(self, extension: str):
        pass


class LVM(Sensor):

    def __init__(self, binding: str, name: str, lv_name: str, vg_name: str):
        self.lv_name = lv_name
        self.vg_name = vg_name
        super(Sensor).__init__(binding=binding, name=name)

    def vg_exists(self):
        pass

    def vg_size(self):
        pass

    def vg_available_space(self):
        pass

    def lv_exists(self):
        pass

    def lv_size(self):
        pass


if __name__ == '__main__':
    pass

