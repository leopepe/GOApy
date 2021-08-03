from goap.WorldState import WorldState
import unittest


class WorldStateTest(unittest.TestCase):
    def setUp(self):
        self.world_state = WorldState({
            'tmp_dir_state': 'not_exist',
            'tmp_dir_content': 'token_not_found'})

    def test_world_state(self):
        assert self.world_state == {
            'tmp_dir_state': 'not_exist',
            'tmp_dir_content': 'token_not_found'
        }
