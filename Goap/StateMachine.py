from Goap.Action import Actions
from Goap.Planner import Planner


class StateMachine:

    def __init__(self, states: Actions):
        """
            Don't need initial and end state since the transition
            will be a ordered list.
        :param states:
        """
        self._states = states
        self._planner = Planner(actions=states)
        self._transitions = []
        self._current_state = None
        self.start_state = None
        self.end_state = None

    def set_transitions(self, init_state, end_state):
        """ Receives an ordered list and set it to self._transitions

        :param planner:
        :param init_state:
        :param end_state:
        :param obj:
        :param obj: obj capable of order the list
        :return: None
        """
        transitions = []
        plan = self._planner.plan(init_state, end_state)
        for src, dst, obj in plan:
            transitions.append(obj['object'])
            # transitions.append(self._states.get(obj['object']['Name']))

        self._transitions = transitions

    def get_transitions(self):
        return self._transitions

    def start(self, printable: bool=False):
        result = []
        for state in self._transitions:
            self._current_state = state
            try:
                result.append(self._current_state.do())
            except:
                raise RuntimeError

        self.stop()

        if printable:
            print(result)

        return result

    def stop(self):
        self._current_state = None


if __name__ == '__main__':
    from Goap import Planner
    import random
    # import pprint
    from time import sleep
    from datetime import datetime
    # ACTIONS
    actions = Actions()
    # monitor state
    actions.add_action(
        name='CheckModules',
        pre_conditions={'vpc_checked': False, 'db_check': False, 'app_checked': False},
        effects={'vpc_checked': True, 'db_check': True, 'app_checked': True}
    )
    # VPC/Network set
    actions.add_action(
        name='CreateVPC',
        pre_conditions={'vpc': False, 'db': False, 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # DB set
    actions.add_action(
        name='CreateDB',
        pre_conditions={'vpc': True, 'db': False, 'app': False},
        effects={'vpc': True, 'db': True, 'app': False}
    )
    actions.add_action(
        name='StopDB',
        pre_conditions={'vpc': True, 'db': 'started', 'app': False},
        effects={'vpc': True, 'db': 'stopped', 'app': False}
    )
    actions.add_action(
        name='StartDB',
        pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
        effects={'vpc': True, 'db': 'started', 'app': False}
    )
    actions.add_action(
        name='DestroyDB',
        pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
        effects={'vpc': True, 'db': False, 'app': False}
    )
    # APP set
    actions.add_action(
        name='CreateApp',
        pre_conditions={'vpc': True, 'db': True, 'app': False},
        effects={'vpc': True, 'db': True, 'app': True}
    )
    actions.add_action(
        name='StartApp',
        pre_conditions={'vpc': True, 'db': True, 'app': True},
        effects={'vpc': True, 'db': True, 'app': 'started'}
    )
    actions.add_action(
        name='AppMaintenance',
        pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
        effects={'vpc': True, 'db': True, 'app': 'maintenance'}
    )
    actions.add_action(
        name='StopApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'maintenance'},
        effects={'vpc': True, 'db': True, 'app': 'stopped'}
    )
    actions.add_action(
        name='StartStoppedApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
        effects={'vpc': True, 'db': True, 'app': 'started'}
    )
    actions.add_action(
        name='DestroyIllApp',
        pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
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
    cases = [case1, case2, case3, case4, case5]
    #
    # FSM
    fsm = StateMachine(states=actions)
    # pprint.pprint(fsm.get_transitions(), indent=2)

    while True:
        print('\n\n\n###\n###\n###')
        print('Starting {}'.format(datetime.now()))
        case = random.choice(cases)
        print('Case: {}'.format(case))
        print('[WARN] Change identified by sensor...')
        print('[INFO] Planning...')
        fsm.set_transitions(init_state=case['init_state'], end_state=case['goal'])
        print('[INFO] Plan: {}'.format(fsm.get_transitions()))
        fsm.start()
        print('Sleeping 7 sec from {}'.format(datetime.now()))
        sleep(7)

