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
        assert 'CreateVPC' in str(self.actions.get(name='CreateVPC').do())

    def test_remove_action_success(self):
        self.actions.remove_action(name='CreateVPC')
        assert [{"Name": "CreateVPC"}] not in self.actions
