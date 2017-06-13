'''
All the enumerations in one place
'''

from enum import IntEnum


class Orientation(IntEnum):
    '''
    Defines how one block is oriented.
    '''
    West = 0    # Towards decreasing X
    East = 1    # Towards increasing X
    South = 2   # Towards decreasing Y
    North = 3   # Towards increasing Y
    Down = 4    # Towards decreasing Z
    Up = 5      # Towards increasing Y


class AliasOrientation(IntEnum):
    '''
    Same as Orientation, but in "context" of a cube
    '''
    Back = 0
    Front = 1
    Right = 2
    Left = 3
    Down = 4
    Up = 5


class Rotation(IntEnum):
    '''
    Defines how the block is oriented.
    Tooghether with Orientation this gives
    24 possibilities to place the block.
    '''
    Up = 0      # 12:00 normal, heading to the sky
    Right = 1   # 15:00 right wall on "earth"
    Down = 2    # 18:00 upside down
    Left = 3    # 21:00 left wall on "earth"


class ServiceTypes(IntEnum):
    '''
    How one behaviour is connected to another? Depends upon block type.
    This should be read as a service type provided by on one behaviour
    to another. The rationale here is to suspend service requests when
    there is no active service provider. So optimisation is the sole
    reason why this enumaration exists.
    '''
    serInternal = 0  # service is not exposed and is not expected to be connected
                     # Don't change "0" since it's used explicitly.
    serProvideItems = 1  # e.g. Box
    serReceiveItems = 2  # e.g. Box
    serPullItems = 3  # e.g. Conveyor
    serPushItems = 4  # e.g. Conveyor
    # serSupplyLiquid = 2
    # serSupplyElectricity = 3
    # serSupplyMechanicalWork = 4
    # serSupplyLabor = 5


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