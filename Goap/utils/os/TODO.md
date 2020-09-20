# TODO

## actions

delete files older than X days
delete files with different from pattern X
delete files with pattern X
compact files older than X days
move files older than X days to path Y
delete files with extension .X
send email notification
start process X
stop process X
increase LVM size in Xmb
start container X
stop container X

## sensors

detect files older than X days
detect files with different from pattern X
detect files with pattern X
detect files with extension .X
detect if volume above X% usage
detect if vg needs more disks
detect if container X is running

```python
class OSFilePath(Sensor):

    def __init__(self, binding: str, name: str, path: str):
        self.path = path
        super().__init__(binding=binding, name=name)

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
        super().__init__(binding=binding, name=name, path=path)

    def exec(self):
        return self.is_dir()


class FileExist(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super().__init__(binding=binding, name=name, path=path)

    def exec(self):
        return self.is_file()


class FileIsOlderThan(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super().__init__(binding=binding, name=name, path=path)

    def is_older(self, days: str):
        pass


class FileNamePattern(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super().__init__(binding=binding, name=name, path=path)

    def has_name_pattern(self):
        pass


class FileHasExtension(OSFilePath):

    def __init__(self, binding: str, name: str, path: str):
        super().__init__(binding=binding, name=name, path=path)

    def has_extension(self, extension: str):
        pass


class LVM(Sensor):

    def __init__(self, biding: str, name: str, vg_name: str, lv_name: str):
        self.lvm = None  # lvm client
        self.binding = biding
        self.vg_name = vg_name
        self.lv_name = lv_name
        super().__init__(binding=self.binding, name=self.name)

    def vg_exists(self):
        try:
            if self.lvm.get_vg(self.vg_name):
                return 'exist'
            else:
                return 'not_exist'
        except LookupError as e:
            raise '{}'.format(e)

    def vg_size(self):
        pass

    def vg_available_space(self):
        pass

    def lv_exists(self):
        pass

    def lv_size(self):
        pass

```