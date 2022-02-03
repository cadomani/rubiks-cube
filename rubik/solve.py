import rubik.cube as rubik
from enum import Enum


class CubeRotations(Enum):
    """ Writing cube rotations as an enum allows us to get direction easily by an even-odd check
        as well as assigning a procedure to an integer value rather than a string, where we can 
        unintentionally fail to compare upper vs lowercase.
    """
    F = 0
    f = 1
    R = 2
    r = 3
    B = 4
    b = 5
    L = 6
    l = 7
    U = 8
    u = 9
    D = 10
    d = 11
    
    
def _solve(parms):
    if parms['rotate'] not in CubeRotations:
        return({
            "status": "error: invalid rotation command provided"
        })
