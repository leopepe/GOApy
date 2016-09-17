class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.initial_state = None
        self.final_state = []

    def add_state(self, name, handler, state=0):
        name = name.upper()
        self.handlers[name] = handler
        if state:
            self.final_state.append(name)

    def set_start(self, name):
        self.initial_state = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.initial_state]
        except:
            raise SystemError('must call .set_start() before .run()')
        if not self.final_state:
            raise SystemError('at least one state must be an end_state')

        while True:
            (new_state, cargo) = handler(cargo)
            if new_state.upper() in self.final_state:
                print('reached ', new_state)
                break
            else:
                handler = self.handlers[new_state.upper()]