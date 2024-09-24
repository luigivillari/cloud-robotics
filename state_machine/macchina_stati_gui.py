
from transitions import Machine
import random

class MacchinaStati(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['have_token', 'have_compose', 'wake_up','execute_compose']

    def __init__(self, name):

        # No anonymous superheroes on my watch! Every narcoleptic superhero gets
        # a name. Any name at all. SleepyMan. SlumberGirl. You get the idea.
        self.name = name

        # What have we accomplished today?
        self.kittens_rescued = 0

        # Initialize the state machine
        self.machine = Machine(model=self, states=MacchinaStati.states, initial='wake_up')

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        self.machine.add_transition(trigger='token_request', source='wake_up', dest='have_token')

        # Superheroes need to keep in shape.
        self.machine.add_transition('compose_request', 'have_token', 'have_compose')

        # Those calories won't replenish themselves!
        self.machine.add_transition('run', 'have_compose', 'execute_compose')

        self.machine.add_transition('compose_request','execute_compose','have_compose')

if __name__ == '__main__':
    narcoleptic_superhero = MacchinaStati('Nodo_Edge')
    print(narcoleptic_superhero.state)
    narcoleptic_superhero.token_request()
    print(narcoleptic_superhero.state)
    narcoleptic_superhero.compose_request()
    print(narcoleptic_superhero.state)
    narcoleptic_superhero.run()
    print(narcoleptic_superhero.state)
    narcoleptic_superhero.compose_request()
    print(narcoleptic_superhero.state)