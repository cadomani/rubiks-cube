import rubik.cube as rubik
from enum import Enum


CUBE_ROTATIONS = [
    "F",
    "f",
    "R",
    "r",
    "B",
    "b",
    "L",
    "l",
    "U",
    "u",
    "D",
    "d"
]
    
    
def _solve(parms):
    if parms['rotate'] not in CUBE_ROTATIONS:
        return({
            "status": "error: invalid rotation command provided"
        })
    return {"status": "ok"}
