import copy
from dataclasses import dataclass
import re
from enum import Enum, unique
from typing import List, Set
from rubik.utils.exceptions import *

CUBE_PIECES = 54
CUBE_FACES = 6
CUBE_FACE_PIECES = 9
CUBE_SHARED_EDGES = 12
CUBE_SHARED_CORNERS = 8


class PieceType(Enum):
    """ Defines the types of pieces available for a 3x3 cube. """
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
    CORNER_C = PieceArrangement(PieceType.CORNER, [9, 16, 48], [8, 15, 47], {0, 1, 5})
    CORNER_D = PieceArrangement(PieceType.CORNER, [7, 46, 36], [6, 45, 35], {0, 3, 5})
    CORNER_E = PieceArrangement(PieceType.CORNER, [19, 12, 39], [18, 11, 38], {1, 2, 4})
    CORNER_F = PieceArrangement(PieceType.CORNER, [21, 37, 28], [20, 36, 27], {2, 3, 4})
    CORNER_G = PieceArrangement(PieceType.CORNER, [27, 34, 52], [26, 33, 51], {2, 3, 5})
    CORNER_H = PieceArrangement(PieceType.CORNER, [25, 54, 18], [24, 53, 17], {1, 2, 5})
    EDGE_A   = PieceArrangement(PieceType.EDGE, [2, 44], [1, 43], {0, 4})
    EDGE_B   = PieceArrangement(PieceType.EDGE, [6, 13], [5, 12], {0, 1})
    EDGE_C   = PieceArrangement(PieceType.EDGE, [8, 47], [7, 46], {0, 5})
    EDGE_D   = PieceArrangement(PieceType.EDGE, [4, 33], [3, 32], {0, 3})
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
    def get_arrangement_from_element(index):
        """ Locate a piece if we know any one of the elements. Index parameter is zero based. """
        for arrangement in CubeArrangement:
            if arrangement.name != 'PieceArrangement' and index in arrangement.true_indexes:
                return arrangement
        return None

    @staticmethod
    def is_valid_adjacency(adjacencies):
        """ Obtain an arrangement from a set of adjacencies. """
        for arrangement in CubeArrangement:
            if arrangement.name != 'PieceArrangement' and adjacencies == arrangement.adjacencies:
                return arrangement
        return None

    @staticmethod
    def get_cohesive_pieces(pieces, color_index, piece_type: PieceType):
        """ Return all the valid edges or corners for the color index. """
        return list(
            filter(
                lambda v: (v.value == color_index) and (v.arrangement.piece_type == piece_type.value),
                pieces
            )
        )

    @staticmethod
    def get_face_pieces(pieces, face: int, piece_type: PieceType):
        """ Return all the valid edges or corners for this face. """
        pieces = list(
            filter(
                lambda v: (v.index // CUBE_FACE_PIECES == face) and v.arrangement.piece_type == piece_type.value,
                pieces
            )
        )
        return sorted(pieces, key=lambda v: v.rm_index)


@dataclass
class CubePiece:
    """
    Models a single cube piece and all the relevant properties.
    The pieces retain their structure and values after instantiation.
    Translations only change the value of the piece.

    index: the cube-index value of this piece, 0-based
    value: the 'color' of this piece (alphanumerical)
    rm_index: the row-major index of this piece
    home_face: the primary face index of this piece
    arrangement: identifies a piece and its arrangement
    adjacent_faces: the neighboring faces of the piece
    """
    index: int
    value: str
    rm_index: int
    home_face: int
    arrangement: CubeArrangement
    adjacent_faces: Set[int]

    def shift(self, new_value):
        """ A small helper that allows shifting of pieces within dataclass while retaining the previous value. """
        temp = self.value
        self.value = new_value
        return temp


class CubeFace(Enum):
    """
    Maps a cube face to its array number, defines the inverse,
    and provides helper methods to access its edges, corners, the center, and its color (identity)

    Functionally, manipulating state is not a common use for enums, but the benefit is that we can easily access and manipulate a single face
    without instantiation, turning this implementation into more of a singleton, which is perfect for this use case.
    """
    F = 0
    R = 1
    B = 2
    L = 3
    U = 4
    D = 5
    _SKIRT_MAP = [(7, 4, 1), (1, 2, 3), (3, 6, 9), (9, 8, 7)]

    def __init__(self, _):
        self._edges = []
        self._corners = []
        self._skirt = []
        self._center = None
        self._color = None

    @property
    def opposite(self):
        return {
            CubeFace.F: CubeFace.B,
            CubeFace.R: CubeFace.L,
            CubeFace.B: CubeFace.F,
            CubeFace.L: CubeFace.R,
            CubeFace.U: CubeFace.D,
            CubeFace.D: CubeFace.U
        }[self]

    @property
    def color(self):
        return self._center.value

    @color.setter
    def color(self, value: str):
        self._color = value

    @property
    def center(self) -> CubePiece:
        return self._center

    @center.setter
    def center(self, value: CubePiece):
        self._center = value
        self.color = value.value

    @property
    def edges(self) -> List[CubePiece]:
        return self._edges

    @edges.setter
    def edges(self, value: List[CubePiece]):
        self._edges = value
        if len(self._corners) > 0:
            self._set_skirt()

    @property
    def corners(self) -> List[CubePiece]:
        return self._corners

    @corners.setter
    def corners(self, value: List[CubePiece]):
        self._corners = value
        if len(self._edges) > 0:
            self._set_skirt()

    def _set_skirt(self):
        """ The skirt is the first row or column of cubes surrounding the current face, it is important because it rotates along with the
            face. Having a consistent definition for the positioning of this area allows us to create generic translations regardless of positioning

            In row major order, the skirt starts from the bottom-left of a cube, and each cube index corresponds to the next mapped area

            CUBE FACE:
            1  2  3
            4  5  6
            7  8  9

            We index the position on the face but use our adjacency map to locate the piece bordering these cubes.
        """
        # Define the skirt map
        skirt_pieces = [*self._edges, *self._corners]
        for group in self._SKIRT_MAP.value:
            skirt_group = []
            for x, edge in enumerate(group):
                # Cubes have clockwise arrangements by design, accessing the second index is only done on the first of each face
                index_pop = 2 if x == 0 else 1

                # Locate a piece that maches the index
                found_piece = list(filter(lambda v: v.rm_index == edge, skirt_pieces))[0]

                # Values need to wrap around differently for corners and edges
                cutoff = 3 if found_piece.arrangement.piece_type == "CORNER" else 2

                # Obtain skirt value indexes
                values = found_piece.arrangement.indexes
                offset = values.index(found_piece.index + 1)
                offset_index = (index_pop + offset) % cutoff
                mapped_value = values[offset_index]

                # Save skirt index within group
                skirt_group.append(mapped_value)
            self._skirt.append(skirt_group)

    def rotate(self, pieces, direction="CW"):
        """ Allows rotation of a single face in a clockwise or anti-clockwise direction"""
        # Rotate face
        temp_corner = self.corners[0].value
        temp_edge = self.edges[0].value
        corner_cw = [0, 2, 3, 1] if direction == "CW" else [0, 1, 3, 2]
        edge_cw = [0, 1, 3, 2] if direction == "CW" else [0, 2, 3, 1]
        for x, (corner, edge) in enumerate(zip(corner_cw, edge_cw)):
            self.corners[corner].value = temp_corner if x == 3 else self.corners[corner_cw[x + 1]].value
            self.edges[edge].value = temp_edge if x == 3 else self.edges[edge_cw[x + 1]].value

        # Rotate skirt
        skirt = self._skirt if direction == "CW" else [self._skirt[0], *self._skirt[:0:-1]]
        for i in range(0, 3):
            temp = pieces[skirt[0][i] - 1].value
            for j in range(1, 5):
                cube_index = skirt[j % 4][i] - 1
                temp = pieces[cube_index].shift(temp)

    @staticmethod
    def translate_rotation(rotation: str, destination_face: int):
        if destination_face == 0:
            return rotation
        elif destination_face == 1:
            return {
                "F": "R",
                "R": "B",
                "B": "L",
                "L": "F",
                "U": "U",
                "D": "D"
            }[rotation]
        elif destination_face == 2:
            return {
                "F": "B",
                "R": "L",
                "B": "F",
                "L": "R",
                "U": "U",
                "D": "D"
            }[rotation]
        elif destination_face == 3:
            return {
                "F": "L",
                "R": "F",
                "B": "R",
                "L": "B",
                "U": "U",
                "D": "D"
            }[rotation]
        elif destination_face == 4:
            return {
                "F": "U",
                "R": "R",
                "B": "D",
                "L": "L",
                "U": "B",
                "D": "F"
            }[rotation]
        elif destination_face == 5:
            return {
                "F": "D",
                "R": "R",
                "B": "U",
                "L": "L",
                "U": "F",
                "D": "B"
            }[rotation]


class Cube:
    """ Provides methods for identifying, querying, and manipulating a 3x3 Rubik's Cube and checking its validity. """
    def __init__(self, input_cube: str):
        # Check validity of input
        if input_cube is None or input_cube == '':
            raise CubeMissing()

        # Test to see if value is a string
        if not isinstance(input_cube, str):
            raise InvalidCubeType(input_cube)

        # Variations on conversion to raw string implies invalid characters
        if len(repr(input_cube)) - 2 != len(input_cube):
            raise InvalidCubeCharacters(input_cube)

        # Test for the actual value length
        if len(input_cube) != CUBE_PIECES:
            raise InvalidCubeLength(input_cube)

        # Check for illegal characters. Match 54 characters containing a-z, A-Z, and 0-9 only using Regex. No match returns None.
        if not re.match(r'[a-zA-Z0-9]{54}', input_cube):
            raise InvalidCubeCharacters(input_cube)

        # Cube parameters
        self._cube_string = input_cube
        self._cube_map: str                 # a 1-to-1 face map of the input string
        self._faces = CubeFace              # identifies all the faces of this cube by index or name
        self._pieces: List[CubePiece] = []  # the individual pieces that make up the cube and their properties
        self._pinned_centerpieces = {}      # to simplify solve, we assume that the central locations of the cube are the permanent faces and can be pinned
        self._remap_pieces()                # convert input string to a same-size string containing the face index for each value
        self._state = [self._cube_string]   # the cube state as a stack of values

        # Create cube object from data received
        self._unpack()

    def _unpack(self):
        # Create a cube object from input to continue validating
        color_map = {}
        for x, (piece_value, mapped_value) in enumerate(zip(self._cube_string, self._cube_map)):
            # Obtain current cube arrangement of the piece provided
            arrangement = CubeArrangement.get_arrangement_from_element(x)
            row_major_index = (x + 1) % CUBE_FACE_PIECES

            # Create a cube piece with the relevant parameters
            piece = CubePiece(
                x,
                piece_value,
                rm_index=(9 if row_major_index == 0 else row_major_index),
                home_face=mapped_value,
                arrangement=arrangement,
                adjacent_faces={self._cube_map[face] for face in arrangement.true_indexes},
            )
            self._add_piece(piece)

            # Add the piece value and index to the color map
            color_map[piece_value] = color_map.get(piece_value, 0) + 1

        # Test for invalid cube conditions post unpack
        for piece, count in color_map.items():
            if count != 9:
                raise InvalidCubeComposition(piece, self)

    def _remap_pieces(self):
        # Retrieve pinned centerpieces by location
        for x, i in enumerate(range(4, 53, 9)):
            self._pinned_centerpieces[self._cube_string[i]] = x

        # Test for non-unique centerpieces
        if self._pinned_centerpieces.__len__() != CUBE_FACES:
            raise InvalidCubeCenter(self)
        self._cube_map = [self._pinned_centerpieces[face] for face in self._cube_string]

    def _add_piece(self, piece: CubePiece):
        # Check boundary conditions before adding piece
        if CubeArrangement.is_valid_adjacency(piece.adjacent_faces) is None:
            if piece.arrangement.piece_type == PieceType.CORNER.value:
                raise InvalidCubeCorner(self)
            elif piece.arrangement.piece_type == PieceType.EDGE.value:
                raise InvalidCubeEdge(self)

            # This error should NOT happen, but if any test matches this output we can retrace
            raise InvalidCubeComposition('center', self)

        # Boundary checks successful, add piece
        self._pieces.append(piece)

        # Trigger update to the faces, corners, and edges once we reach cube length
        if len(self._pieces) == CUBE_PIECES:
            self._update()

    def _update(self):
        """ Once the cube object has been filled, calculate faces, corners, and edges. """
        for i in range(0, CUBE_FACES):
            # Obtain centerpiece, edges, and corners
            self._faces(i).center = CubeArrangement.get_face_pieces(self._pieces, i, PieceType.CENTER)[0]
            self._faces(i).edges = CubeArrangement.get_face_pieces(self._pieces, i, PieceType.EDGE)
            self._faces(i).corners = CubeArrangement.get_face_pieces(self._pieces, i, PieceType.CORNER)

    def rotate(self, rotate_command: List[str] = None):
        # Iterate through rotation commands, updating state each time
        for command in rotate_command:
            # Determine direction by upper/lowercase ascii value
            direction = "CW"
            if ord(command) >= 97:
                direction = "ACW"

            # Perform in-place rotation within face
            self._faces[command.upper()].rotate(self._pieces, direction)

            # Save states to be able to show stages along with final results
            self._reconstruct()
            self._state.append(self._cube_string)

    def solve(self):
        # Check if we qualify for a bottom cross
        centerpiece = self._faces.D.center.value
        for edge in self._faces.D.edges:
            if edge.value != centerpiece:
                break
        else:
            # If we didn't break, all pieces match. No rotations needed
            return ""

        # Wildly inefficient, but okay for a first try
        faces = copy.deepcopy(self._faces)
        pieces = copy.deepcopy(self._pieces)

        # Identify candidates
        solved_configuration = "000000000111111111222222222333333333444444444555555555"
        current_solved = list(filter(lambda v: v.value == centerpiece, faces.D.edges)).__len__()
        candidates = []
        possibilities = CubeArrangement.get_cohesive_pieces(pieces, centerpiece, PieceType.EDGE)
        for possibility in possibilities:
            # Includ pieces in bottom layer only if they are not actually located at the bottom of the cube
            if possibility.index < 45:
                candidates.append(possibility)

        # Create data container to find best match
        matches = {
            "A": [],
            "B": [],
            "C": []
        }

        # Parse through candidates to find best match
        heuristics_A = ['r', 'Dr', 'DDr', 'dr', 'F', 'DF', 'DDF', 'dF', 'L', 'DL', 'DDL', 'dL', 'f', 'Df', 'DDf', 'df']
        heuristics_B = ['FF', 'UFF', 'UUFF', 'uFF', 'Fr', 'fL', 'dFF', 'dFDr']
        heurStd = ['UF', 'UUF', 'uF', 'Uf', 'UUf', 'uf']
        for heur_a in heuristics_A:
            for heur_b in heurStd:
                heuristics_B.append(f"{heur_b}{heur_a}")

        for candidate in candidates:
            # Save current arrangement for easy lookups
            arrangement = candidate.arrangement.name

            # Identify proper configuration by arrangement value
            if "_B" in arrangement or "_F" in arrangement or "_I" in arrangement or "_D" in arrangement in arrangement:
                matches['A'] = Cube._solve_configuration(heuristics_A, candidate, faces, pieces, current_solved, centerpiece)
            elif "_A" in arrangement or "_E" in arrangement or "_H" in arrangement or "_K" in arrangement:
                matches['B'] = Cube._solve_configuration(heuristics_B, candidate, faces, pieces, current_solved, centerpiece)
            elif "_C" in arrangement or "_G" in arrangement or "_J" in arrangement or "_L" in arrangement:
                print("C syle arrangement")
            else:
                print("Unhandled arrangement error")
                return None

        # Visually test solutions
        import pprint
        pprint.pprint(matches)
        original = "".join([f.value for f in self._pieces])
        new_cube = "".join([f.value for f in pieces])
        print(f'original \t{original}')
        print(f'new \t{new_cube}')
        if original != new_cube:
            raise Exception("Cube not returned to default")

        # Find winning rotation
        best = None
        for k, configuration in matches.items():
            for item in configuration:
                if best is None:
                    best = item
                else:
                    if item['success']:
                        if item['set'] >= best['set'] or item['steps'] <= best['steps']:
                            best = item
        return best['heuristic']

    @staticmethod
    def _solve_configuration(heuristics, candidate, faces, pieces, current_set, centerpiece):
        # Try heuristics, log and undo
        matches = []
        for heuristic in heuristics:
            # Iterate through rotation commands, updating state each time
            new_heuristic = ""
            for command in heuristic:
                translated_heuristic = CubeFace.translate_rotation(command.upper(), candidate.index // 9)

                # Determine direction by upper/lowercase ascii value
                direction = "CW"
                if ord(command) >= 97:
                    direction = "ACW"
                    translated_heuristic = translated_heuristic.lower()
                new_heuristic += translated_heuristic

                # Perform in-place rotation within face
                faces[translated_heuristic.upper()].rotate(pieces, direction)

            # Add to a match object to determine viability
            new_set = list(filter(lambda v: v.value == centerpiece, faces.D.edges)).__len__()
            matches.append(
                {
                    "heuristic": new_heuristic,
                    "steps"    : len(heuristic),
                    "success"  : current_set < new_set,
                    "set"      : new_set,
                    "new_cube" : "".join([f.value for f in pieces])
                }
            )

            # Undo operations by reversing heuristic steps and applying the inverse
            for command in reversed(new_heuristic.swapcase()):
                # Determine direction by upper/lowercase ascii value
                direction = "CW"
                if ord(command) >= 97:
                    direction = "ACW"

                # Perform in-place rotation within face
                faces[command.upper()].rotate(pieces, direction)

            # undo changes made to faces
            for i in range(0, CUBE_FACES):
                # Obtain centerpiece, edges, and corners
                faces(i).center = CubeArrangement.get_face_pieces(pieces, i, PieceType.CENTER)[0]
                faces(i).edges = CubeArrangement.get_face_pieces(pieces, i, PieceType.EDGE)
                faces(i).corners = CubeArrangement.get_face_pieces(pieces, i, PieceType.CORNER)
        return matches

    def _reconstruct(self):
        """ Update cube string by appending all cube values in order to a string to save state, and remap (this is useful in case a center turn is ever added). """
        self._cube_string = "".join([f.value for f in self._pieces])
        self._remap_pieces()

    def __str__(self):
        return self._cube_string

    def __repr__(self):
        return f'{self._cube_string}\n{self._cube_map}'
