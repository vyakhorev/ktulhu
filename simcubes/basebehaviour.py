
from simcubes.simcore import cAsyncThread

import logging
logger = logging.getLogger(__name__)


def iter_threads_in_holders(holders):
    '''
    Each cube have behaviours. In order to run them, we need to
    schedule them in the environment. This call heps us to do
    this.
    :param holders: a list of game world objects who inherit
    from cBehaviourHolder.
    '''
    for h_i in holders:
        for thr_i in h_i.behaviours:
            yield thr_i


class cSimulBehaviour(cAsyncThread):
    '''
    Base class for simulation activities. A block can have multiple
    interacting behaviours. So block logic is reponsible only for
    connecting the behaviours with each other.
    '''

    def __init__(self, parent):
        '''
        :param env: simulation environment, to be excluded from __init__ calls
        :param parent: an object from the simulation (a block, a bunch of blocks).
                So parent is a subclass of cBehaviourHolder.
        '''
        super().__init__()
        self.parent = parent
        self.connected = []

    def connect_to(self, other_behaviour, connection_type):
        self.connected += [(connection_type, other_behaviour)]


class cBehaviourHolder:
    '''
    Base class for all simulation blocks and aggregated instances.
    Holds all the behaviours, exposes their variables and states
    as a single callee.

    С++ code doesn't know about behaviours. but it can read the
    variables from here. Oh maybe this is not a good idea..
    '''

    def __init__(self):
        self.behaviours = []

    def add_behaviour(self, behaviour):
        self.behaviours += [behaviour]

