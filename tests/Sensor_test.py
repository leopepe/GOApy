import unittest

from goap.sensor import Sensors


class SensorsTest(unittest.TestCase):

    def setUp(self):
        # ACTIONS
        self.sensors = Sensors()

    def test_add_success(self):
        self.sensors = Sensors()
        self.sensors.add(
            name='FindOldFilesOnTmp',
            shell='find /tmp/log_tests -mtime +1|wc -l|xargs test -f && echo "Exists" || echo "None"',
            binding='old_files'
        )
        self.sensors.add(
            name='LogFilesToCompact',
            shell='test $(find /tmp/log_tests -name "*.log" -type f -size +900M| wc -l) -gt 0 && echo "Exists" || echo "None"',
            binding='old_files'
        )
        assert 'Name: LogFilesToCompact' == str(self.sensors.get(name='LogFilesToCompact'))
        assert 'Name: FindOldFilesOnTmp' == str(self.sensors.get(name='FindOldFilesOnTmp'))

    def test_remove_sensor_success(self):
        assert self.sensors.remove(name='LogFilesToCompact') is True

    def test_remove_sensor_error(self):
        assert self.sensors.remove(name='CreateAPP') is False
