#!/usr/bin/env python
#
#  CreateFullStack  Identifying information about tests here.
#
# ===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

import unittest

from goap.action import Actions


class TestCreateFullStackTestGroupName(unittest.TestCase):

    def setUp(self):
        # ACTIONS
        self.actions = Actions()

        # VPC/Network set
        self.actions.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False},
            shell='awscli vpc create'
        )

        # DB set
        self.actions.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='StartDB',
            pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
            effects={'vpc': True, 'db': 'started', 'app': False},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='StopDB',
            pre_conditions={'vpc': True, 'db': 'started', 'app': False},
            effects={'vpc': True, 'db': 'stopped', 'app': False},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='DestroyDB',
            pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
            effects={'vpc': True, 'db': False, 'app': False},
            shell='awscli vpc create'
        )

        # APP set
        self.actions.add(
            name='CreateApp',
            pre_conditions={'vpc': True, 'db': True, 'app': False},
            effects={'vpc': True, 'db': True, 'app': True},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='StartApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
            effects={'vpc': True, 'db': True, 'app': 'started'},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='StopApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
            effects={'vpc': True, 'db': True, 'app': 'stopped'},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='DestroyApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
            effects={'vpc': True, 'db': True, 'app': False},
            shell='awscli vpc create'
        )

    def tearDown(self):
        # VPC/Network unset
        self.actions.remove(name='CreateVPC')
        # DB unset
        self.actions.remove(name='CreateDB')
        self.actions.remove(name='StartDB')
        self.actions.remove(name='StopDB')
        self.actions.remove(name='DestroyDB')
        # APP unset
        self.actions.remove(name='CreateApp')
        self.actions.remove(name='StartApp')
        self.actions.remove(name='StopApp')
        self.actions.remove(name='DestroyApp')

    def test_CreateFullStack_Test_Create_VPN(self):
        assert 'Name: CreateVPC' == str(self.actions.get(name='CreateVPC'))

    def test_CreateFullStack_Test_Create_DB(self):
        assert 'Name: CreateDB' == str(self.actions.get(name='CreateDB'))

    def test_CreateFullStack_Test_Create_APP(self):
        assert 'Name: CreateApp' == str(self.actions.get(name='CreateApp'))

    def test_CreateFullStack_Test_Create_Size(self):
        self.assertEqual(self.actions.__len__(), 9)


if __name__ == "__main__":
    unittest.main()
