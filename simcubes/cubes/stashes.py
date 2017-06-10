'''
Chests, boxes, liquid tanks e.t.c.
'''

from simcubes.world import cSimCube
from simcubes.en import CubeTypes

from simcubes.behaviours.storage import cBehItemStorage

class cBox(cSimCube):

    def init_behaviours(self):
        self.cube_type = CubeTypes.blBox

        # beh = cBehItemStorage(self)
        # self.add_behaviour(beh)

    def connect(self):
        '''
        connect external behaviours with neighboor behaviours,
        subject to orientation.
        '''
        


