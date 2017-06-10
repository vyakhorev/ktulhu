'''
Environmental threads: blooming, growing, pollution e.t.c.
'''

from simcubes.simcore import cEvent
from simcubes.basebehaviour import cSimulBehaviour

import logging
logger = logging.getLogger(__name__)


class cBehBlooming(cSimulBehaviour):
    '''
    Periodically blooming.
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.is_active = True
        self.is_blooming = False  # ?make this a state

    def run(self):
        while self.is_active:
            self.is_blooming = True
            yield cEvent(self, 0.1)  # a timeout
            self.is_blooming = False
            yield cEvent(self, 0.2)