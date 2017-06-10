'''
Chests, boxes, liquid tanks e.t.c.
'''

from simcubes.world import cSimCube
from simcubes.en import CubeTypes, orientation_to_vector

from simcubes.behaviours.storage import cBehItemStorage

class cBox(cSimCube):

    def init_behaviours(self):
        self.cube_type = CubeTypes.blBox
        # behaviours that push and pull from this block,
        # subject to orientation
        self.pusher = None
        self.puller = None
        beh = cBehItemStorage(self)
        self.add_behaviour(beh)
        self.storage_behaviour = beh

    def connect(self):
        '''
        connect external behaviours with neighboor behaviours,
        subject to orientation.
        '''
        # TODO: This is a very raw code, we'll have to fix it soon
        # Suppose that we can push to the back and to pull
        # from the direction only
        dirvec_f = orientation_to_vector(self.orientation)
        dirvec_b = (-1 * dirvec_f[0], -1 * dirvec_f[1], -1 * dirvec_f[2])
        front_cube = self.world.get_neighbour_by_vector(self, dirvec_f)
        back_cube = self.world.get_neighbour_by_vector(self, dirvec_b)

        # Connect to conveyours

        if not(front_cube is None):
            if hasattr(front_cube, "source") and (self.orientation == front_cube.orientation):
                # Connect to conveyour, must be co-oriented
                front_cube.source = self
                self.puller = front_cube
                # behaviour connections
                self.storage_behaviour.puller_behaviour = front_cube.pull_push_behaviour
                front_cube.pull_push_behaviour.source_behaviour = self.storage_behaviour

        if not (back_cube is None):
            if hasattr(back_cube, "sink") and (self.orientation == back_cube.orientation):
                # Connect to conveyour, must be co-oriented
                back_cube.sink = self
                self.pusher = back_cube
                # behaviour links
                self.storage_behaviour.pusher_behaviour = back_cube.pull_push_behaviour
                back_cube.pull_push_behaviour.sink_behaviour = self.storage_behaviour








        


