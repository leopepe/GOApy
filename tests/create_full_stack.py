#!/usr/bin/env python
#
#  CreateFullStack  Identifying information about tests here.
#
# ===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

import unittest
from goap import Actions


class TestCreateFullStackTestGroupName(unittest.TestCase):

    def setUp(self):
        # ACTIONS
        self. actions = Actions()

        # VPC/Network set
        self.actions.add_action(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )

        # DB set
        self.actions.add_action(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        self.actions.add_action(
            name='StartDB',
            pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
            effects={'vpc': True, 'db': 'started', 'app': False}
        )
        self.actions.add_action(
            name='StopDB',
            pre_conditions={'vpc': True, 'db': 'started', 'app': False},
            effects={'vpc': True, 'db': 'stopped', 'app': False}
        )
        self.actions.add_action(
            name='DestroyDB',
            pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )

        # APP set
        self.actions.add_action(
            name='CreateApp',
            pre_conditions={'vpc': True, 'db': True, 'app': False},
            effects={'vpc': True, 'db': True, 'app': True}
        )
        self.actions.add_action(
            name='StartApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
            effects={'vpc': True, 'db': True, 'app': 'started'}
        )
        self.actions.add_action(
            name='StopApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
            effects={'vpc': True, 'db': True, 'app': 'stopped'}
        )
        self.actions.add_action(
            name='DestroyApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
            effects={'vpc': True, 'db': True, 'app': False}
        )

    def tearDown(self):
        # VPC/Network unset
        self.actions.remove_action(name='CreateVPC')
        # DB unset
        self.actions.remove_action(name='CreateDB')
        self.actions.remove_action(name='StartDB')
        self.actions.remove_action(name='StopDB')
        self.actions.remove_action(name='DestroyDB')
        # APP unset
        self.actions.remove_action(name='CreateApp')
        self.actions.remove_action(name='StartApp')
        self.actions.remove_action(name='StopApp')
        self.actions.remove_action(name='DestroyApp')

    def test_CreateFullStack_Test_Create_VPN(self):
        self.assertEqual(self.actions.get(name='CreateVPC').do(), ('CreateVPC', True))

    def test_CreateFullStack_Test_Create_DB(self):
        self.assertEqual(self.actions.get(name='CreateDB').do(), ('CreateDB', True))

    def test_CreateFullStack_Test_Create_APP(self):
        self.assertEqual(self.actions.get(name='CreateApp').do(), ('CreateApp', True))

    def test_CreateFullStack_Test_Create_Size(self):
        self.assertEqual(self.actions.__len__(), 9)


if __name__ == "__main__":
    unittest.main()
