import unittest

from Goap.Sensor import Sensors


class SensorsTest(unittest.TestCase):
    def setUp(self):
        # ACTIONS
        self.sensors = Sensors()

    def test_add_success(self):
        self.sensors.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False},
            shell='awscli vpc create'
        )
        self.sensors.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False},
            shell='awscli rds create'
        )
        assert 'Name: CreateVPC' == str(self.sensors.get(name='CreateVPC'))
        assert 'Name: CreateDB' == str(self.sensors.get(name='CreateDB'))

    def test_remove_sensor_success(self):
        self.sensors.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        self.sensors.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        self.sensors.remove(name='CreateVPC')
        assert 'Name: CreateDB' == str(self.sensors.get(name='CreateDB'))

    def test_remove_sensor_error(self):
        self.sensors.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        self.sensors.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        self.sensors.remove(name='CreateAPP')
        assert 'None' == str(self.sensors.get(name='CreateAPP'))
