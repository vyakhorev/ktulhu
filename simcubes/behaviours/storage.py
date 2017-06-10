'''
Different aspects of storage and delivery
'''


from simcubes.simcore import cEvent
from simcubes.basebehaviour import cSimulBehaviour
from simcubes.en import ResourceTypes

import logging
logger = logging.getLogger(__name__)

class cBehItemStorage(cSimulBehaviour):
    '''
    Stores an item
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.item_type = ResourceTypes.resCoal
        self.quantity = 0  #int
        self.is_active = True  # TODO: this must be a state
        self.pusher_behaviour = None  #this is very raw, to be changed ASAP
        self.puller_behaviour = None

    def put(self, quantity):
        self.quantity += quantity
        logger.info("Put " + str(quantity) + " of " + str(self.item_type))

    def get(self, quantity):
        self.quantity -= quantity
        logger.info("Took " + str(quantity) + " of " + str(self.item_type))

    def run(self):
        while self.is_active:
            logger.info('hosting items')
            yield cEvent(self, 0.3)  # a timeout
            yield cEvPut(self, 0.01, 10)
            yield cEvGet(self, 0.01, 5)


class cBehItemPullPush(cSimulBehaviour):
    '''
    Pull from a storage and push to the storage
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.item_type = ResourceTypes.resCoal
        self.buffer = 0 # how many items in the storage
        self.is_active = True
        # Connected behaviours
        # Both may be either cBehItemStorage or cBehItemPullPush
        self.source_behaviour = None
        self.sink_behaviour = None

    def run(self):
        while self.is_active:
            logger.info('pulling and pushing')
            yield cEvent(self, 0.1)


class cEvPut(cEvent):

    priority = 1

    def __init__(self, beh, duration, quantity):
        super().__init__(beh, duration)
        self.quantity = quantity

    def apply(self):
        # we can do this with a wrapper function and a callback
        self.beh.put(self.quantity)


class cEvGet(cEvent):

    priority = 2

    def __init__(self, beh, duration, quantity):
        super().__init__(beh, duration)
        self.quantity = quantity

    def apply(self):
        # we can do this with a wrapper function and a callback
        self.beh.get(self.quantity)