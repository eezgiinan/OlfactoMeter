from state import State


class RestingState(State):

    def on_event(self, order, countdown):
        if countdown == 0:
            return UnlockedState()
        else if:

        else:
            return

        return self
