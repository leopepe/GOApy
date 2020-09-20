from Goap.utils.os.ShellCommand import ShellCommand


def test_all():
    ls = ShellCommand('ls -ltra')
    if ls:
        assert True
