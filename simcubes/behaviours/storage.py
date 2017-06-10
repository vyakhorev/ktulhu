'''
Different aspects of storage and delivery
'''


from simcubes.simcore import cEvent
from simcubes.basebehaviour import cSimulBehaviour

import logging
logger = logging.getLogger(__name__)

class cBehItemStorage(cSimulBehaviour):

    def __init__(self, parent):
        super().__init__(parent)
        self.item_type = None
        self.quantity = 0  #int
        self.is_active = True

    def put(self, quantity):
        self.quantity += quantity
        #logger.info("Put " + str(quantity) + " of " + str(self.item_type))

    def get(self, quantity):
        self.quantity -= quantity
        #logger.info("Took " + str(quantity) + " of " + str(self.item_type))

    def run(self):
        while self.is_active:
            yield cEvent(self, 0.1)  # a timeout
            yield cEvPut(self, 0.00, 10)
            yield cEvGet(self, 0.00, 5)


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