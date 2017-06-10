'''
Different kind of grounds, including ores.
'''

from simcubes.world import cSimCube
from simcubes.en import CubeTypes

from simcubes.behaviours.eco import cBehBlooming

class cGrass(cSimCube):

    def init_behaviours(self):
        self.cube_type = CubeTypes.blGrass
        beh = cBehBlooming(self)
        self.add_behaviour(beh)


