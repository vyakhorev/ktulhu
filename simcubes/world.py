
from simcubes.basebehaviour import cBehaviourHolder
from simcubes.en import orientation_to_vector

import logging
logger = logging.getLogger(__name__)


class cSimWorld:
    '''
    The whole world. A main class to generate, save, load, interact with simcubes.
    '''
    def __init__(self):
        '''
        chunks holds links to all the blocks
        active_chunk - active element from self.chunks
        '''
        self.chunks = {}
        self.active_chunk_id = None

    def set_active_chunk(self, chunk_id):
        '''
        Call this every time you switch between chunks
        :param chunk_id: active chunk id
        '''
        if not(chunk_id in self.chunks):
            self.chunks[chunk_id] = {}
        self.active_chunk_id = chunk_id

    def add_block(self, new_game_block):
        '''
        Add block to the active chunk
        :param new_game_block: a new game block, with a generated gid.
        '''
        # TODO: generate gid
        # TODO: save chunk as a reference
        new_game_block.world = self
        self.chunks[self.active_chunk_id][new_game_block.gid] = new_game_block

    def get_neighbour_by_direction(self, cube, direction):
        '''
        Get the neighbour to the cube in the given direction (in the active chunk)
        :param cube: some cube that's already in the world
        :param direction: find a cube in this direction (member of Orientation)
                (relative to the cube's direction), 1 step over the axis.
        :return: a cube or None
        '''
        dirvec = orientation_to_vector(direction)
        return self.get_neighbour_by_vector(cube, dirvec)

    def get_neighbour_by_vector(self, cube, dirvec):
        '''
        Get the neighbour to the cube in the given direction (in the active chunk)
        :param dirvec: an offset vector like (1, 0, 0)
        :return: a cube or None
        '''
        thischunk = self.chunks[self.active_chunk_id]
        desired_coords = (cube.x + dirvec[0], cube.y + dirvec[1], cube.z + dirvec[2])
        # TODO: we need a hashmap with coordinates for an active chunk
        for cube_i in thischunk.values():
            if cube_i.get_coords() == desired_coords:
                return cube_i
        return None

    def iter_over_blocks(self):
        '''
        Iterates over all the blocks in the world (debug purposes)
        '''
        for ch_i in self.chunks.values():
            for bl_i in ch_i.values():
                yield bl_i

    def get_debug_string(self):
        '''
        Debug only
        '''
        s = "A sim world with blocks: \n"
        for i, chunk_i in self.chunks.items():
            s += "\n*** CHUNK num" + str(i) + ":\n"
            for bl in chunk_i.values():
                s += "\t" + bl.get_debug_string() + "\n"
        return s

class cSimCube(cBehaviourHolder):
    '''
    Represents a simulation block in the game.
    Each struct GameBlock from UE4 has a link to such a simulation
    block - this makes it easy to update it.
    This thing is inherented by concrete realisations.
    '''
    def __init__(self, gid=0, x=0, y=0, z=0, cube_type=0, orientation = 0):
        '''
        :param gid: game id of the block, same as in the game
        :param x, y, z: game coordinates, normalised.
        :param block_type: a string to setup behaviour
        behaviours: a list with simulation logic (read state from there)
        '''
        super().__init__()
        self.gid = gid
        self.x = x
        self.y = y
        self.z = z
        self.cube_type = cube_type
        self.orientation = orientation
        self.world = None
        self.init_behaviours()

    def init_behaviours(self):
        '''
        Implement initialisation routines here. Would be called at __init__
        '''
        raise NotImplemented

    def get_debug_string(self):
        return "Block of type " + str(self.cube_type) + " num" + str(self.gid) + " at " + str(self.x) + "," + str(self.y) + "," + str(self.z)

    def set_gid(self, gid):
        self.gid = gid

    def get_coords(self):
        '''
        :return: (x, y, z) as a tuple
        '''
        return self.x, self.y, self.z

    def set_coords(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_orientation(self, orientation):
        self.orientation = orientation

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z