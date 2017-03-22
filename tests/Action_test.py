import unittest

from Goap import Actions


class ActionTest(unittest.TestCase):
    def setUp(self):
        # ACTIONS
        self.actions = Actions()

    def test_add_action_success(self):
        self.actions.add_action(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        self.actions.add_action(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        assert '{"Name": "CreateVPC"}' == str(self.actions.get(name='CreateVPC'))
        assert '{"Name": "CreateDB"}' == str(self.actions.get(name='CreateDB'))

    def test_remove_action_success(self):
        self.actions.add_action(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        self.actions.add_action(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        self.actions.remove_action(name='CreateVPC')
        assert 'None' == str(self.actions.get(name='CreateVPC'))
        assert '{"Name": "CreateDB"}' == str(self.actions.get(name='CreateDB'))

    def test_remove_action_error(self):
        self.actions.add_action(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        self.actions.add_action(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        self.actions.remove_action(name='CreateAPP')
        assert '{"Name": "CreateVPC"}' == str(self.actions.get(name='CreateVPC'))
        assert '{"Name": "CreateDB"}' == str(self.actions.get(name='CreateDB'))
        assert 'None' == str(self.actions.get(name='CreateAPP'))
