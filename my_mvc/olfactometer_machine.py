from statemachine import StateMachine, State
from my_modes import Odors

class OlfactometerMachine(StateMachine):
    """Olfactometer Project State Machine"""
#    [State(name=odor, value=odor.index(odor) + 3) for odor in odor_names]

    resting = State('Resting', initial=True, value=1)
    purging = State('Purging', value=2)
    delivering_1 = State('Delivering ' + Odors.Odor_1.value, value=3)
    delivering_2 = State('Delivering ' + Odors.Odor_2.value, value=4)

    purge = resting.to(purging) | delivering_1.to(purging) | delivering_2.to(purging)
    deliver_1 = purging.to(delivering_1) | resting.to(delivering_1)
    deliver_2 = purging.to(delivering_2) | resting.to(delivering_2)
