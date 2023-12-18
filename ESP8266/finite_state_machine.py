class FiniteStateMachine(object):
    def __init__(self):
        self.main_state_loop = ["MAIN"]
        self.extra_states = ["SHOW_QUOTE", "VOICE_RECOG"]
        self.current_state = self.main_state_loop[0]
        return
    
    def next_state(self):
        '''
        Loop among self.main_state_loop
        '''
        if self.current_state not in self.main_state_loop:
            self.current_state = self.main_state_loop[0]
        else:
            current_index = self.main_state_loop.index(self.current_state)
            next_index = (current_index + 1) % (len(self.main_state_loop))
            self.current_state = self.main_state_loop[next_index]
        return self.current_state

    def jump_to_state(self, state: str):
        assert state in self.main_state_loop + self.extra_states, "State not exists"
        self.current_state = state
        return self.current_state