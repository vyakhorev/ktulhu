'''
All the enumerations in one place
'''

from enum import IntEnum


class Orientation(IntEnum):
    '''
    Defines how one block is orientated
    '''
    East = 0    # Towards decreasing X
    West = 1    # Towards increasing X
    South = 2   # Towards decreasing Y
    North = 3   # Towards increasing Y
    Down = 4    # Towards decreasing Z
    Up = 5      # Towards increasing Y


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
    resWheat = 10