from goap.utils.os.shell_command import ShellCommand


def test_command_output():
    echo = ShellCommand('printf success')
    output = echo()
    assert output[0] == 'success'
