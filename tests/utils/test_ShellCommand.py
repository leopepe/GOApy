from Goap.utils.os.ShellCommand import ShellCommand


def test_command_output():
    echo = ShellCommand('printf success')
    output = echo()
    assert output[0] == 'success'
