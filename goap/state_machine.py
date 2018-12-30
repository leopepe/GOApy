from goap.action import Actions
from goap.planner import Planner as Plan


class StateMachine:
    def __init__(self, states: Actions):
        """
            Don't need initial and end state since the transition
            will be a ordered list.
        :param states:
        """
        self._states = states
        self._planner = Plan(actions=states)
        self._transitions = []
        self._current_state = None
        self.start_state = None
        self.end_state = None

    def set_transitions(self, init_state: dict, end_state: dict):
        """ Receives an ordered list and set it to self._transitions

        :param init_state: A dict representing the initial state of the StateMachine
        :param end_state: A dict representing the final state of the StateMachine
        :return: None
        """
        transitions = []
        if init_state in self._planner.actions.all_possible_states():
            plan = self._planner.plan(init_state, end_state)
            print(plan)
            for src, dst, obj in plan:
                transitions.append(obj['object'])
        self._transitions = transitions

    def get_transitions(self):
        return self._transitions

    def stop(self):
        self._current_state = None
        # sys.exit(1)

    def start(self, init_state: dict, end_state: dict):
        result = []
        self.set_transitions(init_state=init_state, end_state=end_state)
        for state in self._transitions:
            self._current_state = state
            result.append(self._current_state.do())

        self.stop()
        return result


if __name__ == '__main__':
    import random
    # import pprint
    from time import sleep
    from datetime import datetime

    # ACTIONS
    actions = Actions()
    # monitor state
    actions.add(
        name='CheckModules',
        pre_conditions={'vpc_checked': False, 'db_check': False, 'app_checked': False},
        effects={'vpc_checked': True, 'db_check': True, 'app_checked': True}
    )
    # VPC/Network set
    actions.add(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # DB set
    actions.add(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    actions.add(
        name='StopDB',
        pre_conditions={'vpc': True, 'db': 'started', 'app': False},
        effects={'vpc': True, 'db': 'stopped', 'app': False}
    )
    actions.add(
        name='StartDB',
        pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
        effects={'vpc': True, 'db': 'started', 'app': False}
    )
    actions.add(
        name='DestroyDB',
        pre_conditions={'vpc': True, 'db': 'unhealthy', 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # APP set
    actions.add(
        name='CreateApp',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': True, 'app': True}
    )
    actions.add(
        name='StartApp',
        pre_conditions={'vpc': True, 'db': True, 'app': True},
        effects={'vpc': True, 'db': True, 'app': 'started'}
    )
    actions.add(
        name='AppMaintenance',
        pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
        effects={'vpc': True, 'db': True, 'app': 'maintenance'}
    )
    actions.add(
        name='StopApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'maintenance'},
        effects={'vpc': True, 'db': True, 'app': 'stopped'}
    )
    actions.add(
        name='StartStoppedApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': 'started'}
    )
    actions.add(
        name='DestroyIllApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'unhealthy'},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    #
    # Test cases scenarios
    case1 = {
        'init_state': {'vpc': False, 'db': False, 'app': False},
        'goal': {'vpc': True, 'db': True, 'app': True}
    }
    case2 = {
        'init_state': {'vpc': True, 'db': False, 'app': False},
        'goal': {'vpc': True, 'db': True, 'app': 'stopped'}
    }
    case3 = {
        'init_state': {'vpc_checked': False, 'db_check': False, 'app_checked': False},
        'goal': {'vpc_checked': True, 'db_check': True, 'app_checked': True}
    }
    case4 = {
        'init_state': {'vpc': True, 'db': False, 'app': False},
        'goal': {'vpc': True, 'db': True, 'app': False}
    }
    case5 = {
        'init_state': {'vpc': True, 'db': True, 'app': 'maintenance'},
        'goal': {'vpc': True, 'db': True, 'app': 'started'}
    }
    case6 = {
        'init_state': {'vpc': False, 'db': False, 'app': True},
        'goal': {'vpc': True, 'db': True, 'app': True}
    }
    cases = [case1, case2, case3, case4, case5]
    #
    # FSM
    fsm = StateMachine(states=actions)
    # pprint.pprint(fsm.get_transitions(), indent=2)

    while True:
        print('\n\n\n###\n###\n###')
        print('Starting {}'.format(datetime.now()))
        case = random.choice(cases)
        # case = case6
        print('Case: {}'.format(case))
        print('[WARN] Change identified by sensor...')
        print('[INFO] Planning...')
        fsm.start(init_state=case['init_state'], end_state=case['goal'])
        print('Sleeping 7 sec from {}'.format(datetime.now()))
        sleep(7)
