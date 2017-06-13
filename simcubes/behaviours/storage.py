'''
Different aspects of storage and delivery
'''


import logging

from simcubes.behaviours.basebehaviour import cSimulBehaviour
from simcubes.en import ResourceTypes
from simcubes.simcore import cEvent

logger = logging.getLogger(__name__)

class cBehItemStorage(cSimulBehaviour):
    '''
    Stores an item
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.item_type = ResourceTypes.resCoal
        self.quantity = 0  #int

    def run(self):
        while self.is_active:
            logger.info('hosting items')
            yield cEvent(self, 0.3)  # a timeout


class cBehItemPullPush(cSimulBehaviour):
    '''
    Pull from a storage and push to the storage
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.item_type = ResourceTypes.resCoal
        self.buffer = 0 # how many items in the storage

    def run(self):
        while self.is_active:
            logger.info('pulling and pushing')
            yield cEvent(self, 0.1)


# class cEvPut(cEvent):
#
#     priority = 1
#
#     def __init__(self, beh, duration, quantity):
#         super().__init__(beh, duration)
#         self.quantity = quantity
#
#     def apply(self):
#         # we can do this with a wrapper function and a callback
#         self.beh.put(self.quantity)
#
#
# class cEvGet(cEvent):
#
#     priority = 2
#
#     def __init__(self, beh, duration, quantity):
#         super().__init__(beh, duration)
#         self.quantity = quantity
#
#     def apply(self):
#         # we can do this with a wrapper function and a callback
#         self.beh.get(self.quantity)
