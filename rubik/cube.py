from dataclasses import dataclass
import re
from enum import Enum, unique
from typing import List, Set, Dict
from functools import cache


# CUBE ERRORS
class CubeError(BaseException):
    def __init__(self, error, problem_cube):
        self._error = error
        self._cube = problem_cube

    def __str__(self):
        return self._error

    def __repr__(self):
        return f'{self._error} with input \n\t{self._cube}'


class CubeMissing(CubeError):
    def __init__(self):
        super().__init__('error: the cube parameter is missing', None)


class InvalidCubeComposition(CubeError):
    def __init__(self, problem_face, problem_cube):
        super().__init__(f'error: the "{problem_face}" face value does not occur 9 times', problem_cube)


class InvalidCubeDeclaration(CubeError):
    def __init__(self, subissue, problem_cube):
        super().__init__(f'error: invalid cube declaration - {subissue}', problem_cube)


class InvalidCubeLength(InvalidCubeDeclaration):
    def __init__(self, problem_cube):
        super().__init__(f'the cube is not 54 characters in length', problem_cube)


class InvalidCubeType(InvalidCubeDeclaration):
    def __init__(self, problem_cube):
        super().__init__(f'the cube value is not a string', problem_cube)


class InvalidCubeCharacters(InvalidCubeDeclaration):
    def __init__(self, problem_cube):
        super().__init__(f'the cube contains invalid characters', problem_cube)


class InvalidCubeConfiguration(CubeError):
    """ Base Exception for errors occurring due to an unsolvable configuration of cube pieces. """
    def __init__(self, subissue, problem_cube):
        super().__init__(f'error: invalid cube configuration - {subissue}', problem_cube)


class InvalidCubeCenter(InvalidCubeConfiguration):
    def __init__(self, problem_cube):
        super().__init__(f'the cube does not contain six unique center pieces', problem_cube)


class InvalidCubeEdge(InvalidCubeConfiguration):
    def __init__(self, problem_cube):
        super().__init__(f'the cube does not contain a valid arrangement of edge pieces', problem_cube)


class InvalidCubeCorner(InvalidCubeConfiguration):
    def __init__(self, problem_cube):
        super().__init__(f'the cube does not contain a valid arrangement of corner pieces', problem_cube)


@unique
class CubeFace(Enum):
    """ Maps a cube face to its array number, and defines its inverse. """
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    UP = 4
    DOWN = 5

    @property
    def opposite(self):
        return {
            CubeFace.FRONT: CubeFace.BACK,
            CubeFace.RIGHT: CubeFace.LEFT,
            CubeFace.BACK: CubeFace.FRONT,
            CubeFace.LEFT: CubeFace.RIGHT,
            CubeFace.UP: CubeFace.DOWN,
            CubeFace.DOWN: CubeFace.UP
        }[self]


@unique
class CubeArrangement(Enum):
    """ Models relationsips for the cube
        Values start at index 1 and must be reduced

        Corners: 8 (A-H)
        Edges: 1 or cube_index2 (A-L)
        Centers: 6 (A-F)
    """
    CORNER_A = [1, 30, 43]
    CORNER_B = [3, 45, 10]
    CORNER_C = [7, 46, 36]
    CORNER_D = [9, 16, 48]
    CORNER_E = [19, 12, 39]
    CORNER_F = [21, 37, 28]
    CORNER_G = [25, 54, 18]
    CORNER_H = [27, 34, 52]
    EDGE_A = [2, 44]
    EDGE_B = [4, 33]
    EDGE_C = [6, 13]
    EDGE_D = [8, 47]
    EDGE_E = [11, 42]
    EDGE_F = [15, 22]
    EDGE_G = [17, 51]
    EDGE_H = [20, 38]
    EDGE_I = [24, 31]
    EDGE_J = [26, 53]
    EDGE_K = [29, 40]
    EDGE_L = [35, 49]
    CENTER_A = [5]
    CENTER_B = [14]
    CENTER_C = [23]
    CENTER_D = [32]
    CENTER_E = [41]
    CENTER_F = [50]
    CORNER = 'CORNER'
    EDGE = 'EDGE'
    CENTER = 'CENTER'

    @property
    def piece_type(self):
        if self.name.startswith(self.CENTER.value):
            return self.CENTER
        elif self.name.startswith(self.CORNER.value):
            return self.CORNER
        return self.EDGE

    @classmethod
    def match(cls, cube_index):
        for arrangement in list(cls):
            if (cube_index + 1) in arrangement.value:
                return arrangement


@dataclass
class CubePiece:
    index: int                      # The cube-index value of this piece
    value: str                      # The value of this piece
    rm_index: int                   # The row-major index of this piece
    face: CubeFace                  # The face identity enum of this piece
    opposite: CubeFace              # The face identity of the point on the other side of the board
    arrangement: CubeArrangement    # Identifies an edge piece
    parity: int = 0                 # The parity of the edge or corner piece


class CubeObj:
    def __init__(self):
        self._faces: Set[str] = set()
        self._edges: Dict[str] = {}
        self._corners: Dict[str] = {}
        self._pieces: List[CubePiece] = []

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        return self._edges

    @property
    def corners(self):
        return self._corners

    @property
    def pieces(self):
        return self._pieces

    def add_piece(self, piece: CubePiece):
        self._pieces.append(piece)

        # Trigger update to the faces, corners, and edges once we reach cube length
        if len(self._pieces) == 54:
            self._update()

    def _update(self):
        # Reset original fields
        self._faces = set()
        self._corners = {}
        self._edges = {}

        # Recalculate
        for x, piece in enumerate(self._pieces):
            # Add face values
            if (x + 1) % 9 == 5:
                self._faces.add(piece.value)

    @cache
    def _get_arrangement(self, face: int, arrangement_type: CubeArrangement):
        return list(
            filter(
                lambda v: v.face == CubeFace(face) and v.arrangement.piece_type == arrangement_type,
                self._pieces
            )
        )

    @cache
    def get_center_by_cube_index(self, index):
        return self._get_arrangement((index // 9), CubeArrangement.CENTER)[0]

    @cache
    def get_center_by_face(self, index):
        return self._get_arrangement(index, CubeArrangement.CENTER)[0]

    @cache
    def get_corners(self, face_index):
        return self._get_arrangement(face_index, CubeArrangement.CORNER)


class Cube:
    """ Rubik's cube object

        Provides methods for identifying, querying, and manipulating a cube and checking its validity
    """
    def __init__(self, values):
        self._cube_string = values
        self._center_pieces = set()
        self._cube = CubeObj()

        # Check validity of input
        if self._cube_string is None:
            raise CubeMissing()

        # Test to see if value is a string
        if not isinstance(self._cube_string, str):
            raise InvalidCubeType(self._cube_string)

        # Test for the value length
        if not len(self._cube_string) == 54:
            raise InvalidCubeLength(self._cube_string)

        # Check for illegal characters. Match 54 characters containing a-z, A-Z, and 0-9 only using Regex. No match returns None.
        if not re.match(r'[a-zA-Z0-9]{54}', self._cube_string):
            raise InvalidCubeCharacters(self._cube_string)

        # Create a cube object from this input to continue validating
        self._input_to_cube_object()

        # EC: Verify that the positioning of the elements in the cube is valid by
        if not self._is_valid_arrangement():
            raise InvalidCubeCorner(self._cube_string)

    def _input_to_cube_object(self):
        included = {}
        for x, value in enumerate(self._cube_string):
            # Instead of a 4-line if statement, we take advantage of the dictionary's get method to return a value of 0 if the key does not exist and add one to increment
            included[value] = included.get(value, 0) + 1

            # In the same loop, we collect the modulo 9 of each key and the face value
            face = x // 9
            rm_index = (x + 1) % 9

            # Add the cube piece to our object
            piece = CubePiece(
                x,
                value,
                rm_index=rm_index,
                face=CubeFace(face),
                opposite=CubeFace(face).opposite,
                arrangement=CubeArrangement.match(x),
                parity=CubeArrangement.match(x).value.index(x + 1)
            )
            self._cube.add_piece(piece)

        # We enumerate through object we created before and check that every key occurs exactly 9 times, this has the side effect of checking that values are unique too
        for face in self._cube.faces:
            if list(filter(lambda v: v.value == face, self._cube.pieces)).__len__() != 9:
                raise InvalidCubeComposition(face, self._cube_string)

        # Test if we had 6 unique center values.
        if len(self._cube.faces) != 6:
            raise InvalidCubeCenter(self._cube_string)

    def _is_valid_arrangement(self):
        """ Test to see if a partially-solved cube has invalid positions.

            Algorithm:
            1. Identify centerpoints and iterate through them
            2. Identify centerpoint face pieces and corner elements
            3. Identify centerpoint facce corner elements and the boundary pieces
            4. Locate centerpoint and opposing face color.
            5. If face color matches corner elements, it is invalid
        """
        # Enumeration for pieces in order F, R, B, L, U, B
        for x in range(0, 6):
            valid = self._valid_face_boundaries(
                self._cube.get_center_by_face(x).value,
                self._cube.get_center_by_face(CubeFace(x).opposite.value).value,
                self._cube.get_corners(x),
            )
            if not valid:
                return False
        return True

    @staticmethod
    def _to_row_major(cube_index):
        """ Return the value as an index from 1 to 9. """
        return 9 if cube_index % 9 == 0 else cube_index % 9

    @staticmethod
    def _to_cube_index(face_index, row_major_value):
        """ Return the value as a cube index from 1 to 54. """
        return (face_index * 9) + row_major_value

    @staticmethod
    def _to_face_index(cube_index):
        return cube_index // 9

    def _valid_face_boundaries(self, primary_piece: str, opposite_piece: str, corner_pieces: List[CubePiece]):
        """ Assert that a single corner of the cube is valid given its positioning.

            Key:
            Any corners containing the same value as the primary piece should not have any values that
            are the same as the opposite piece.
        """
        for corner in corner_pieces:
            corner_values = [self._cube.pieces[v - 1].value for v in corner.arrangement.value]
            for neighbor in corner_values:
                if neighbor == opposite_piece and primary_piece in corner_values:
                    return False
        return True

    def _corner_indexes_to_values(self, corners):
        """ Obtain cube values from respective cube indexes. """
        new_corners = []
        for corner in corners:
            corner_values = []
            for value in corner:
                corner_values.append(self._cube_string[value - 1])
            new_corners.append(corner_values)
        return new_corners

    def __str__(self):
        return self._cube
