'''
Chests, boxes, liquid tanks e.t.c.
'''

from simcubes.world import cSimCube
from simcubes.en import CubeTypes, ServiceTypes

from simcubes.behaviours.storage import cBehItemStorage

class cBox(cSimCube):

    def init_behaviours(self):
        self.cube_type = CubeTypes.blBox
        # This behaviour is registered twice. This would help other
        # processes to decide how to communicate with this block.
        beh = cBehItemStorage(self)
        self.register_behaviour(beh, ServiceTypes.serProvideItems)
        self.register_behaviour(beh, ServiceTypes.serReceiveItems)

    def expose_cubewall_provided_service_types(self, rel_orientation):
        '''
        This block can provide items in all directions and receive items in all directions
        '''
        return [ServiceTypes.serProvideItems, ServiceTypes.serReceiveItems]

    def expose_cubewall_requested_service_types(self, rel_orientation):
        '''
        This block doesn't need anything to operate
        '''
        return None


        


