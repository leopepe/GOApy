from typing import Optional
import unittest

from Goap.utils.os.ShellCommand import ShellCommand
from Goap.Action import Actions, Action
from Goap.Errors import ActionAlreadyInCollectionError


class ActionTest(unittest.TestCase):
    def setUp(self):
        # ACTIONS
        self.actions = Actions()
        self.ls = ShellCommand('ls -ltr /tmp/')
        self.echo = ShellCommand('echo output')

    def test_add_action(self):
        self.actions.add(
            name='create_dir',
            pre_conditions={'dir': False},
            effects={'dir': True},
            cost=0.1,
            func=ShellCommand('/bin/sh -c "ls -ltr /tmp/"')
        )
        create_dir = self.actions.get(name='create_dir')
        self.assertTrue(create_dir)

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

    def test_remove_existing_action(self):
        self.actions.add(
            name='create_gcp',
            pre_conditions={'gcp_account_status': 'exist'},
            effects={'gcp_account_status': 'exist'},
            cost=0.1,
            func=ShellCommand("/bin/sh -c 'echo create_gcp_account'")
        )
        self.actions.remove(name='create_vpc')
        assert not self.actions.get(name='CreateDB')

    def test_remove_non_existing_action(self):
        self.actions.remove(name='CreateAPP')
        self.assertIsNone(self.actions.get(name='CreateAPP'))

    def test_get_by_precondition(self):
        self.actions.add(
            name='ls_call_home',
            pre_conditions={'directories': 'None'},
            effects={'directories': 'some_dirs'},
            cost=0.1,
            func=ShellCommand('ls $HOME')
        )
        self.actions.add(
            name='create_vpc',
            pre_conditions={'vpc_status': 'exist'},
            effects={'vpc_status': 'exist'},
            cost=0.1,
            func=ShellCommand("/bin/sh -c 'echo create_vpc'")
        )
        actions = self.actions.get_by_pre_conditions(
            pre_conditions={'directories': 'None'}
        )
        assert len(actions) == 1

    def test_get_by_effects(self):
        self.actions.add(
            name='dummy',
            pre_conditions={'dummy': 'None'},
            effects={'dummy': 'some_dirs'},
            cost=0.1,
            func=ShellCommand('ls $HOME')
        )
        self.actions.add(
            name='dummy2',
            pre_conditions={'vpc_status': 'exist'},
            effects={'vpc_status': 'exist'},
            cost=0.1,
            func=ShellCommand("/bin/sh -c 'echo create")
        )
        actions = self.actions.get_by_effects(
            effects={'vpc_status': 'exist'}
        )
        assert len(actions) == 1

    def test_unique_action_name(self):
        self.actions.add(
            name='create_gcp',
            pre_conditions={'gcp_account_status': 'exist'},
            effects={'gcp_account_status': 'exist'},
            cost=0.1,
            func=ShellCommand("/bin/sh -c 'echo create_gcp_account'")
        )
        with self.assertRaises(ActionAlreadyInCollectionError):
            self.actions.add(
                name='create_gcp',
                pre_conditions={'gcp_account_status': 'exist'},
                effects={'gcp_account_status': 'exist'},
                cost=0.1,
                func=ShellCommand("/bin/sh -c 'echo create_gcp_account'")
            )

    def test_fail_call_action(self):
        self.actions.add(
            name="failed",
            pre_conditions={'state': 'none'},
            effects={'state': 'done'},
            cost=0.1,
            func=ShellCommand(command='exit 1')
        )
        fail = self.actions.get('failed')
        output = fail()
        assert output.return_code == 1

    def test_call_action(self):
        self.actions.add(
            name="echo",
            pre_conditions={'state': 'none'},
            effects={'state': 'done'},
            cost=0.1,
            func=self.echo
        )
        echo: Optional[Action] = self.actions.get('echo')
        output = echo()
        assert output.response == 'output'
        assert output.return_code == 0
