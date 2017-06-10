'''
Conveyors, ?roads
'''

from simcubes.world import cSimCube
from simcubes.en import CubeTypes

from simcubes.behaviours.storage import cBehItemStorage

class cConveyor(cSimCube):

    def init_behaviours(self):
        self.cube_type = CubeTypes.blConveyor
        # beh = cBehItemStorage(self)
        # self.add_behaviour(beh)
