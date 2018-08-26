from os import listdir
from os.path import isdir, exists


class Directory(object):

    @classmethod
    def content(cls, path: str):
        return ''.join(str(i + '\n') for i in listdir(path))

    @classmethod
    def is_dir(cls, path: str):
        if isdir(path):
            return 'is_dir'
        else:
            return 'not_dir'

    @classmethod
    def exists(cls, path: str):
        if exists(path):
            return 'exist'
        else:
            return 'not_exist'


if __name__ == '__main__':
    print(Directory.exists('/tmp'))
    print(Directory.is_dir('/tmp'))
    print(Directory.content('/tmp'))
