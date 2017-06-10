'''
Conveyors, ?roads
'''

from simcubes.world import cSimCube
from simcubes.en import CubeTypes, orientation_to_vector

from simcubes.behaviours.storage import cBehItemPullPush

class cConveyor(cSimCube):

    def init_behaviours(self):
        self.cube_type = CubeTypes.blConveyor
        # Connected behaviours
        self.source = None  # may be a cConveyor or cBox
        self.sink = None    # may be a cConveyor or cBox
        beh = cBehItemPullPush(self)
        self.add_behaviour(beh)
        self.pull_push_behaviour = beh

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

        if not(front_cube is None):
            if hasattr(front_cube, "source") and (self.orientation == front_cube.orientation):
                # Conveyor case, must be co-oriented
                self.sink = front_cube
                front_cube.source = self
                # behaviour connections
                self.pull_push_behaviour.sink_behaviour = front_cube.pull_push_behaviour
                front_cube.pull_push_behaviour.source_behaviour = self.pull_push_behaviour
            if hasattr(front_cube, "pusher") and (self.orientation == front_cube.orientation):
                # Box case, must be co-oriented
                front_cube.pusher = self
                self.sink = front_cube
                # behaviour connections
                self.pull_push_behaviour.sink_behaviour = front_cube.source_behaviour
                front_cube.storage_behaviour.pusher_behaviour = self.pull_push_behaviour

        if not (back_cube is None):
            if hasattr(back_cube, "sink") and (self.orientation == back_cube.orientation):
                # Conveyor case, must be co-oriented
                self.source = back_cube
                back_cube.sink = self
                # behaviour connections
                self.pull_push_behaviour.source_behaviour = back_cube.pull_push_behaviour
                back_cube.pull_push_behaviour.sink_behaviour = self.pull_push_behaviour
            if hasattr(back_cube, "pusher") and (self.orientation == back_cube.orientation):
                # Box case, must be co-oriented
                self.source = back_cube
                back_cube.sink = self
                # Behaviour connections
                self.pull_push_behaviour.source_behaviour = back_cube.storage_behaviour
                back_cube.storage_behaviour.puller_behaviour = self.pull_push_behaviour


