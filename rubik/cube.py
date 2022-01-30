from dataclasses import dataclass
import re
from enum import Enum, unique
from typing import List, Set
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
    def __init__(self, piece_face, piece_type, problem_cube):
        super().__init__(f'error: the "{piece_face}" {piece_type} value does not occur 9 times', problem_cube)


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


class PieceType(Enum):
    CORNER = "CORNER"
    EDGE = "EDGE"
    CENTER = "CENTER"


@unique
class CubeArrangement(Enum):
    """
    Models relationsips for the cube
    Values start at index 1 and must be reduced
    TODO: These face boundaries are perfectly modeled by a Q3 Hypercube, consider implementing a graph algorithm if these lookups become expensive.

    Corners: 8 (A-H)
    Edges: 1 or cube_index2 (A-L)
    Centers: 6 (A-F)
    """
    @dataclass
    class PieceArrangement:
        """
        Adds a structure to each identifiable piece.

        piece_type: "CORNER", "EDGE", or "CENTER"
        indexes: the 1-based index of the cube
        true_indexes: the 0-based indexes of the cube
        adjacencies: the faces that this piece is adjacent to
        """
        piece_type: PieceType
        indexes: List[int]
        true_indexes: List[int]
        adjacencies: Set[int]

    CORNER_A = PieceArrangement(PieceType.CORNER, [1, 30, 43], [0, 29, 42], {0, 4, 3})
    CORNER_B = PieceArrangement(PieceType.CORNER, [3, 45, 10], [2, 44, 9], {0, 1, 4})
    CORNER_C = PieceArrangement(PieceType.CORNER, [7, 46, 36], [6, 45, 35], {0, 3, 5})
    CORNER_D = PieceArrangement(PieceType.CORNER, [9, 16, 48], [8, 15, 47], {0, 1, 5})
    CORNER_E = PieceArrangement(PieceType.CORNER, [19, 12, 39], [18, 11, 38], {1, 2, 4})
    CORNER_F = PieceArrangement(PieceType.CORNER, [21, 37, 28], [20, 36, 27], {2, 3, 4})
    CORNER_G = PieceArrangement(PieceType.CORNER, [25, 54, 18], [24, 53, 17], {1, 2, 5})
    CORNER_H = PieceArrangement(PieceType.CORNER, [27, 34, 52], [26, 33, 51], {2, 3, 5})
    EDGE_A   = PieceArrangement(PieceType.EDGE, [2, 44], [1, 43], {0, 4})
    EDGE_B   = PieceArrangement(PieceType.EDGE, [4, 33], [3, 32], {0, 3})
    EDGE_C   = PieceArrangement(PieceType.EDGE, [6, 13], [5, 12], {0, 1})
    EDGE_D   = PieceArrangement(PieceType.EDGE, [8, 47], [7, 46], {0, 5})
    EDGE_E   = PieceArrangement(PieceType.EDGE, [11, 42], [10, 41], {1, 4})
    EDGE_F   = PieceArrangement(PieceType.EDGE, [15, 22], [14, 21], {1, 2})
    EDGE_G   = PieceArrangement(PieceType.EDGE, [17, 51], [16, 50], {1, 5})
    EDGE_H   = PieceArrangement(PieceType.EDGE, [20, 38], [19, 37], {2, 4})
    EDGE_I   = PieceArrangement(PieceType.EDGE, [24, 31], [23, 30], {2, 3})
    EDGE_J   = PieceArrangement(PieceType.EDGE, [26, 53], [25, 52], {2, 5})
    EDGE_K   = PieceArrangement(PieceType.EDGE, [29, 40], [28, 39], {3, 4})
    EDGE_L   = PieceArrangement(PieceType.EDGE, [35, 49], [34, 48], {3, 5})
    CENTER_A = PieceArrangement(PieceType.CENTER, [5], [4], {0})
    CENTER_B = PieceArrangement(PieceType.CENTER, [14], [13], {1})
    CENTER_C = PieceArrangement(PieceType.CENTER, [23], [22], {2})
    CENTER_D = PieceArrangement(PieceType.CENTER, [32], [31], {3})
    CENTER_E = PieceArrangement(PieceType.CENTER, [41], [40], {4})
    CENTER_F = PieceArrangement(PieceType.CENTER, [50], [49], {5})

    @property
    def piece_type(self):
        return self.value.piece_type.value

    @property
    def adjacencies(self):
        return self.value.adjacencies

    @property
    def true_indexes(self):
        return self.value.true_indexes

    @property
    def indexes(self):
        return self.value.indexes

    @staticmethod
    @cache
    def get_arrangement_from_element(index):
        """ Locate a piece if we know any one of the elements. Index parameter is zero based. """
        for arrangement in CubeArrangement:
            if arrangement.name != 'PieceArrangement' and index in arrangement.true_indexes:
                return arrangement
        return None

    @staticmethod
    def is_valid_adjacency(adjacencies):
        """ Obtain an arrangement from a set of adjacencies. Cache speeds up operation as set is fully hashable. """
        for arrangement in CubeArrangement:
            if arrangement.name != 'PieceArrangement' and adjacencies == arrangement.adjacencies:
                return arrangement
        return None

    @staticmethod
    def get_pieces(pieces, piece_type: PieceType, index: int = None):
        """ Return all the valid edges or corners for this face. If no index is given, return all edges"""
        return list(
            filter(
                lambda v: (v.face == index if index is not None else True) and v.arrangement.piece_type == piece_type.value,
                pieces
            )
        )


@dataclass
class CubePiece:
    """
    Models a single cube piece and all the relevant properties

    index: the cube-index value of this piece, 0-based
    value: the 'color' of this piece
    rm_index: the row-major index of this piece
    face: the primary face index of this piece
    arrangement: identifies a piece and its arrangement
    adjacent_faces: the neighboring faces of the piece
    final_arrangement: identifies the mapped arrangement of this piece by its final position
    """
    index: int
    value: str
    rm_index: int
    face: int
    arrangement: CubeArrangement
    adjacent_faces: Set[int]
    final_arrangement: CubeArrangement or None = None


class CubeFace(Enum):
    """
    Maps a cube face to its array number, defines the inverse,
    and provides helper methods to access its edges, corners, the center, and its color (identity)
    TODO: This should be a class ideally, not an enum (functionally there is no difference, but we are manipulating instance states)
    """
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    UP = 4
    DOWN = 5

    def __init__(self, _):
        self._edges = []
        self._corners = []
        self._center = None
        self._color = None

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

    @property
    def color(self):
        return self._center.value

    @color.setter
    def color(self, value: str):
        self._color = value

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value: CubePiece):
        self._center = value
        self.color = value.value

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value: List[CubePiece]):
        self._edges = value

    @property
    def corners(self):
        return self._corners

    @corners.setter
    def corners(self, value: List[CubePiece]):
        self._corners = value


class CubeObj:
    """ Defines a cube object and provides methods to access and manipulate the cube. """
    def __init__(self, input_cube: str):
        """
        Receives an input_cube string and converts it to a cube object to be manipulated

        _cube_string: an alias of input_cube
        _cube_map: a 1-to-1 face map of the input string
        _faces: identifies all the faces of this cube by index or name
        _pieces: the individual pieces that make up the cube and their properties
        _pinned_centerpieces: to simplify solve, we assume that the central locations of the cube are the permanent faces and can be pinned
        _color_map: a dictionary of each color and the number of items for each
        """
        self._cube_string = input_cube
        self._cube_map = None
        self._faces = CubeFace
        self._pieces: List[CubePiece] = []
        self._pinned_centerpieces = {}
        self._map_pieces()

        # Convenience object
        self.color_map = {}

        # Create cube object from data received
        self._unpack()

    def _unpack(self):
        # Create a cube object from input to continue validating
        for x, value in enumerate(self._cube_string):
            # Add the cube piece to our object
            arrangement = CubeArrangement.get_arrangement_from_element(x)
            adjacent_faces = set()
            for face in arrangement.true_indexes:
                adjacent_faces.add(self.face_map[face])
            self.color_map[value] = self.color_map.get(value, 0) + 1

            # Construct a piece object to add to the cube
            piece = CubePiece(
                x,
                value,
                rm_index=(x + 1) % 9,
                face=self.get_face_index(value),
                arrangement=arrangement,
                adjacent_faces=adjacent_faces
            )
            self.add_piece(piece)

    def _map_pieces(self):
        for x, i in enumerate(range(4, 53, 9)):
            self._pinned_centerpieces[self._cube_string[i]] = x

        # Test for non-unique centerpieces
        if self._pinned_centerpieces.__len__() != 6:
            raise InvalidCubeCenter(self)
        self._cube_map = [self._pinned_centerpieces[face] for face in self._cube_string]

    def get_face_index(self, value):
        return self._pinned_centerpieces[value]

    @property
    def face_map(self):
        return self._cube_map

    @property
    def faces(self):
        return self._faces

    @property
    def pieces(self):
        return self._pieces

    def add_piece(self, piece: CubePiece):
        # Check boundary conditions before adding piece
        if CubeArrangement.is_valid_adjacency(piece.adjacent_faces) is None:
            if piece.arrangement.piece_type == PieceType.CORNER.value:
                raise InvalidCubeCorner(self)
            elif piece.arrangement.piece_type == PieceType.EDGE.value:
                raise InvalidCubeEdge(self)

            # This error should NOT happen, but if any test matches this output we can retrace
            raise InvalidCubeComposition('x', 'center', self)

        # Boundary checks successful, add piece
        self._pieces.append(piece)

        # Trigger update to the faces, corners, and edges once we reach cube length
        if len(self._pieces) == 54:
            self._update()

    def _update(self):
        """ Once the cube object has been filled, calculate faces, corners, and edges. """
        for i in range(0, 6):
            self._faces(i).center = CubeArrangement.get_pieces(self._pieces, PieceType.CENTER, i)[0]
            self._faces(i).edges = CubeArrangement.get_pieces(self._pieces, PieceType.EDGE, i)
            self._faces(i).corners = CubeArrangement.get_pieces(self._pieces, PieceType.CORNER, i)

    def __str__(self):
        return self._cube_string

    def __repr__(self):
        return f'{self._cube_string}\n{self._cube_map}'


class Cube:
    """ Rubik's cube object

        Provides methods for identifying, querying, and manipulating a cube and checking its validity

        Definitions:
            Face - The 9 contiguous or non-contiguous set of pieces on a cube
            Color - The value of a given face (centerpiece)
            Index - Zero-based index of the cube
            v_index - value of the piece for visual purposes
    """
    def __init__(self, values):
        # Check validity of input
        if values is None:
            raise CubeMissing()

        # Test to see if value is a string
        if not isinstance(values, str):
            raise InvalidCubeType(values)

        # Test for the value length
        if not len(values) == 54:
            raise InvalidCubeLength(values)

        # Check for illegal characters. Match 54 characters containing a-z, A-Z, and 0-9 only using Regex. No match returns None.
        if not re.match(r'[a-zA-Z0-9]{54}', values):
            raise InvalidCubeCharacters(values)

        # Define a cube using the input value
        self._cube = CubeObj(values)

        # Test for invalid cube conditions
        for piece, count in self._cube.color_map.items():
            if count != 9:
                raise InvalidCubeComposition(piece, 'face', self._cube)

    def __str__(self):
        return self._cube
