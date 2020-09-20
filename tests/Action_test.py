import unittest

from Goap.utils.ShellCommand import ShellCommand
from Goap.Action import Actions, Action


class ActionTest(unittest.TestCase):
    def setUp(self):
        # ACTIONS
        self.actions = Actions()
        self.create_db = Action(
            name='create_db',
            pre_conditions={'db_status': 'exist'},
            effects={'db_status': 'exist'},
            cost=0.2,
            func=ShellCommand("/bin/sh -c 'echo create_vpc'")
        )

    def test_add_action(self):
        create_dir = Action(
            name='create_dir',
            pre_conditions={'dir': False},
            effects={'dir': True},
            cost=0.1,
            func=ShellCommand('/bin/sh -c "ls -ltr /tmp/"')
        )
        self.actions.add(action=create_dir)
        print(f"Actions {self.actions}")
        assert True

    def test_add_multiple_actions(self):
        actions = [
            Action(
                name='create_dir',
                pre_conditions={'dir': False},
                effects={'dir': True},
                cost=0.1,
                func=ShellCommand('/bin/sh -c "ls -ltr /tmp/"')
            ),
            Action(
                name='create_vpc',
                pre_conditions={'vpc_status': 'exist'},
                effects={'vpc_status': 'exist'},
                cost=0.1,
                func=ShellCommand("/bin/sh -c 'echo create_vpc'")
            )
        ]
        self.actions = Actions(actions=actions)
        assert len(self.actions) == 2

    def test_remove_action_success(self):
        self.actions.add(
            Action(
                name='create_vpc',
                pre_conditions={'vpc_status': 'exist'},
                effects={'vpc_status': 'exist'},
                cost=0.1,
                func=ShellCommand("/bin/sh -c 'echo create_vpc'")
            )
        )
        self.actions.remove(name='create_vpc')
        assert "None" == str(self.actions.get(name='CreateDB'))

    def test_remove_action_error(self):
        self.actions.remove(name='CreateAPP')
        assert 'None' == str(self.actions.get(name='CreateAPP'))
