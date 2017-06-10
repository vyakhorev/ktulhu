'''
All the enumerations in one place
'''

from enum import IntEnum


class Orientation(IntEnum):
    '''
    Defines how one block is orientated
    '''
    West = 0    # Towards decreasing X
    East = 1    # Towards increasing X
    South = 2   # Towards decreasing Y
    North = 3   # Towards increasing Y
    Down = 4    # Towards decreasing Z
    Up = 5      # Towards increasing Y

def orientation_to_vector(o):
    '''
    :param o: a member of Orientation
    :return: a tuple (x,y,z) directing towards the
             orientation. Like (1, 0, 0)
    '''
    if o == Orientation.West:
        return -1, 0, 0
    if o == Orientation.East:
        return 1, 0, 0
    if o == Orientation.South:
        return 0, -1, 0
    if o == Orientation.North:
        return 0, 1, 0
    if o == Orientation.Down:
        return 0, 0, -1
    if o == Orientation.Up:
        return 0, 0, 1
    raise BaseException('Unhandled direction!')

def vector_to_orientation(vec):
    '''
    :param vec: a tuple, (x, y, z), like (1, 0, 0)
    :return: a member of Orientation
    '''
    if vec == (-1, 0, 0):
        return Orientation.West
    if vec == (1, 0, 0):
        return Orientation.East
    if vec == (0, -1, 0):
        return Orientation.South
    if vec == (0, 1, 0):
        return Orientation.North
    if vec == (0, 0, -1):
        return Orientation.Down
    if vec == (0, 0, 1):
        return Orientation.Up
    raise BaseException('Unhandled direction!')

class Connections(IntEnum):
    '''
    How one behaviour is connected to another? Depends upon block type.
    '''
    pass


class CubeTypes(IntEnum):
    '''
    Cube types, "bl" for easier finding
    '''
    blBedRock = 1
    blGrass = 2
    blSand = 3
    blWater = 4
    blWood = 5
    blBox = 6
    blCornFarm = 7
    blConveyor = 8


class ResourceTypes(IntEnum):
    '''
    Resource types, "res" for easier finding
    '''
    resWater = 1
    resCoal = 2
    resWheat = 10