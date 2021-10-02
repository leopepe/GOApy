from typing import Callable
import unittest

from goap.Sensor import Sensors, Sensor
from goap.utils.os.shell_command import ShellCommand


class SensorResponseTest(unittest.TestCase):
    pass


class SensorTest(unittest.TestCase):
    def setUp(self):
        self.ls = ShellCommand('/bin/sh -c "ls -ltr /tmp/"')
        self.stat_tmp_dir = Sensor(
            name='SenseTmpDir', binding='dir_state', func=self.ls)

    def test_sensor_exec(self):
        response = self.stat_tmp_dir()
        assert response.return_code == 0


class SensorsTest(unittest.TestCase):

    def setUp(self):
        # ACTIONS
        self.sensors = Sensors()
        self.check_dir = ShellCommand(
            command='if [ -d "/tmp/goap_tmp" ]; then printf  "exist"; else printf  "not_exist"; fi'
        )

        self.tmp_dir_state = ShellCommand(
            'if [ -d "/tmp/goap_tmp" ]; then printf  "exist"; else printf  "not_exist"; fi')

    def tearDown(self) -> None:
        self.sensors = []

    def test_add_success(self):
        self.sensors.add(
            name='SenseTmpDirContent2',
            func=ShellCommand(
                '[ -f /tmp/goap_tmp/.token ] && printf  "token_found" || printf  "token_not_found"'),
            binding='tmp_dir_content2'
        )
        print(self.sensors)
        sense_tmp_dir_content2 = self.sensors.get(name='SenseTmpDirContent2')
        assert sense_tmp_dir_content2

    def test_remove_sensor_success(self):
        self.sensors.add(
            name='SenseTmpDirState',
            func=self.tmp_dir_state,
            binding='tmp_dir_state'
        )
        self.assertTrue(self.sensors.remove(name='SenseTmpDirState'))

    def test_remove_sensor_error(self):
        self.assertFalse(self.sensors.remove(name='CreateAPP'))

    def test_run_all(self):
        self.sensors.add(
            name='test_run_all',
            binding='test_result',
            func=self.check_dir
        )
        response = self.sensors.run_all()
        assert str(response) == '[Response: not_exist, ReturnCode: 0]'
