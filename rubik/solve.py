import rubik.cube as rubik
from enum import Enum
import re


class SolveError(BaseException):
    def __init__(self, error, problem_cube, rotate_command):
        self._error = error
        self._cube = problem_cube
        self._rotate = rotate_command

    def __str__(self):
        return self._error

    def __repr__(self):
        return f'{self._error} with input \n\tcube "{self._cube}" - rotate command "{self._rotate}"'


class MissingCube(SolveError):
    def __init__(self, rotate_command):
        super().__init__("error: the cube parameter is missing", None, rotate_command)


class MissingRotateCommand(SolveError):
    def __init__(self, problem_cube):
        super().__init__("error: the rotate command is missing", problem_cube, None)


class InvalidRotateCommand(SolveError):
    def __init__(self, problem_cube, rotate_command):
        super().__init__("error: the rotate command is invalid", problem_cube, rotate_command)


class MissingParameters(SolveError):
    def __init__(self):
        super().__init__("error: both a cube and a rotation parameter must be provided", None, None)


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

VALID_ROTATIONS_REGEX = r"[FfRrBbLlUuDd]"
    
    
def _solve(parms):
    # Pull both required parameters
    cube = parms.get('cube')
    rotate_command = parms.get('rotate')

    # Ensure parameters are not empty
    if cube is None and rotate_command is None:
        raise MissingRotateCommand(rotate_command)

    # Match valid characters
    matches = re.findall(VALID_ROTATIONS_REGEX, rotate_command)

    if len(matches) != len(rotate_command):
        raise InvalidRotateCommand
    if parms['rotate'] not in CUBE_ROTATIONS:
        return({
            "status": "error: invalid rotation command provided"
        })
    return {"status": "ok"}
