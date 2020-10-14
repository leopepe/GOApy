from typing import Callable
import unittest

from Goap.Sensor import Sensors, Sensor
from Goap.utils.os.ShellCommand import ShellCommand


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
            command='if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi'
        )

        self.tmp_dir_state = ShellCommand(
            'if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi')

    def test_add_success(self):
        self.sensors.add(
            name='SenseTmpDirContent2',
            func=ShellCommand(
                '[ -f /tmp/goap_tmp/.token ] && echo -n "token_found" || echo -n "token_not_found"'),
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
        assert self.sensors.remove(name='SenseTmpDirState') is True

    def test_remove_sensor_error(self):
        assert self.sensors.remove(name='CreateAPP') is False
