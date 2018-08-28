import unittest

from Goap.Action import Actions


class ActionTest(unittest.TestCase):
    def setUp(self):
        # ACTIONS
        self.actions = Actions()

    def test_add_action_success(self):
        self.actions.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False},
            shell='awscli vpc create'
        )
        assert 'Name: CreateVPC' == str(self.actions.get(name='CreateVPC'))
        assert 'Name: CreateDB' == str(self.actions.get(name='CreateDB'))

    def test_remove_action_success(self):
        self.actions.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False},
            shell='awscli vpc create'
        )
        self.actions.remove(name='CreateVPC')
        assert 'Name: CreateDB' == str(self.actions.get(name='CreateDB'))

    def test_remove_action_error(self):
        self.actions.add(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False},
            shell='awscli vpc create'
        )
        self.actions.add(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False},
            shell='awscli vpc create'
        )
        self.actions.remove(name='CreateAPP')
        assert 'None' == str(self.actions.get(name='CreateAPP'))
