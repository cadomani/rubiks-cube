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
class HeuristicsProperties:
    """ Container for properties and constants needed to perform repeatable operations on a cube to solve a given face. 
        order: the stage order of this cube operation
        pieces_to_set: the number of pieces that should be solved before this phase is considered complete
        heuristics: a key-value mapping of base algorithmic operations from a front perspective for the given phase
        adjustment_rotations: the type of rotation that should be performed if a piece needs adjustments to match up with other pieces
        adjustment_exclusion: lists the heuristic keys for which we should exclude adjustment rotations
        translation_parameters: a list of callables that can be used to gather the context from which the cube should identify proxy pieces
        arrangement_heuristic: a mapping for which heuristic should be chosen based on the target context pieces
        success_metric: a list of pieces that show completion if they are arranged correctly when checked
        heuristic_strength: using a pure heuristic approach, which heuristic should be chosen first if multiple candidates are valid (no longer used)
    """
    order: int
    pieces_to_set: int
    heuristics: dict
    adjustment_rotations: list
    adjustment_exclusion: list
    translation_parameters: dict
    arrangement_heuristic: dict
    success_metric: list
    heuristic_strength: dict


class CubeHeuristics(Enum):
    """ This enumeration is used as a container for all phases of operations needing heuristic or algorithmic analysis used to solve a cube.
        Each phase is constructed using the HeuristicProperties dataclass, and should be self sufficient to solve any input cube given a list of candidates.
    """
    BottomCross = HeuristicsProperties(
        order=0,
        pieces_to_set=4,
        heuristics={
            'F' : [
                ['', 'FF', 'F', 'f'],
                ['ULfl', 'luLFF', 'RUrFF', 'FluLFF']
            ],
            'R': [
                ['RF', 'RRF', 'rF'],
                ['RUFF', 'RRUFF', 'rUFF', 'UFF']
            ],
            'L': [
                ['Lfl', 'LLfll', 'lf'],
                ['luLFF', 'lulFF', 'luFF', 'uFF', 'LulFF']
            ],
            'U' : [
                ['UUFF'],
                ['UrF']
            ],
            'B': [
                ['BBUUFF'],
                ['bLuFF', 'BrUFF']
            ]
        },
        adjustment_rotations=[],
        adjustment_exclusion=[],
        translation_parameters={
            'F': lambda face, v: face != (0 + v) % 4,
            'R': lambda face, v: face == (1 + v) % 4,
            'L': lambda face, v: face == (3 + v) % 4,
            'U': lambda face, _: face == 4,
            'B': lambda face, _: face == 5
        },
        arrangement_heuristic={
            'R' : ['EFG',   'HIJ',  'KDL',  'ABC'],
            'L' : ['IKL',   'ADC',  'EBG',  'HFJ'],
            'U' : ['H',     'K',    'A',    'E'],
            'F' : ['ABCD',  'BEFG', 'FHIJ', 'DIKL'],
            'B' : ['J',     'L',    'C',    'B']
        },
        success_metric=[
            CubeArrangement.EDGE_C,
            CubeArrangement.EDGE_G,
            CubeArrangement.EDGE_J,
            CubeArrangement.EDGE_L
        ],
        heuristic_strength={
            '0' : 1,
            '1': 0,
            '2' : 0,
            '3': 0
        }
    )
    LowerLayer = HeuristicsProperties(
        order=1,
        pieces_to_set=4,
        heuristics={
            'LIFT': [
                ['RUr'],
                ['BUb'],
                ['LUl'],
                ['FUf']
            ],
            'F': ['fuF'],
            'R': ['ufUF'],
            'U': ['URUUrURur']
        },
        adjustment_rotations=['U'],
        adjustment_exclusion=[],
        translation_parameters={
            'LIFT': lambda face, _: 0,
            'SET': lambda face, _: 0,
            'U': lambda face, v: face != (0 + v) % 4,
            'R': lambda face, v: face == (1 + v) % 4,
            'F': lambda face, v: face == (3 + v) % 4,
        },
        arrangement_heuristic={
            'LIFT': ['C', 'H', 'G', 'D'],
            'SET': ['B', 'E', 'F', 'A'],
        },
        success_metric=[
            CubeArrangement.CORNER_C,
            CubeArrangement.CORNER_H,
            CubeArrangement.CORNER_G,
            CubeArrangement.CORNER_D
        ],
        heuristic_strength={
            '0': 1,
            '1': 0,
            '2': 0,
            '3': 0
        }
    )

    def get_operation(self, face, target):
        """ Utility wrapper for less verbose access to data. """
        return self.value.arrangement_heuristic[face][target]

    def get_algorithm_by_arrangement(self, candidates, target, reference_face):
        """ Takes in a list of candidates, the target face, and the reference value, and returns one or more algorithms that will be 
            pertinent in solving a single candidat on the current phase given a list of potential candidates. The most likely of which is
            chosen to be solved based on context.
        """
        # The heuristic we will try
        if self.name == "BottomCross":
            # Find a candidate for this piece
            candidate_order, candidate = self.locate_match(candidates, self.value.success_metric[target], reference_face)

            # Exit with no algorithm as piece is already solved
            if candidate_order == -1:
                return "", self.value.success_metric[target]

            
            # If the piece is already on the front of the cube, perform adjustment moves to correct
            for face in self.value.arrangement_heuristic:
                if any(f'EDGE_{point}' in candidate.arrangement.name for point in self.get_operation(face, target)):
                    alt = self.value.translation_parameters[face](candidate.current_face, target)
                    return CubeHeuristics.translate_heuristics(
                        self.value.heuristics[face][0 if alt else 1],
                        target,
                        ['']
                    ), self.value.success_metric[target]
        elif self.name == "LowerLayer":
            # Check if we're below and need adjustments to raise to top, or if we're above
            if candidate.arrangement in self.value.success_metric:
                # Candidate piece is at the bottom of the cube
                lift_heur = self.value.heuristics['LIFT'][candidate_order][0]
                rot_heur = "" + "u" * abs(target - (candidate_order - 1))
                if candidate.current_face == 5:
                    face = "F"
                elif candidate.rm_index == 7:
                    face = "R"
                elif candidate.rm_index == 9:
                    face = 'U'

                adj_heur = CubeHeuristics.translate_heuristics(
                    self.value.heuristics[face],
                    target,
                    ['']
                )

                # Combine lift, rotation, and adjustment heuristics
                return [self.minimize(f"{lift_heur}{rot_heur}{adj_heur[0]}")], self.value.success_metric[target]
            else:
                # Find out how many spaces we need to rotate the top to line up with the bottom piece
                rot_heur = "" + "u" * abs(target - self.value.arrangement_heuristic['SET'].index(candidate.arrangement.name.split('_')[1]))

                # Candidate piece is on top of the cube
                if candidate.current_face == 4:
                    heur = self.value.heuristics['U'][0]

                # Piece is on the side of the face if the row-major index is 1, otherwise, it is at the front
                elif candidate.rm_index == 1:
                    heur = self.value.heuristics['R'][0]
                    # rot_heur += "U"
                else:
                    heur = self.value.heuristics['F'][0]

                # Apply rotations in context with the current face
                return CubeHeuristics.translate_heuristics(
                        [self.minimize(f"{rot_heur}{heur}")],
                        target,
                        ['']
                    ), self.value.success_metric[target]

    @staticmethod
    def minimize(moves: str):
        """ The last step before returning the algorithm is minimization of the output rotations list
            Values that are minimized include:
                XXX --> x
                xxx --> X
                Xx  --> Remove
                xX  --> Remove
                
            This function does NOT recursively minimize, however, so values such as 
                XXxxXXxx
            do not get minimized, the expectation is that the algorithm selection doesn't lead to strings like this, and if it might,
            this function can be called in segments or wrapped several times.
        """
        letters = ["f", "u", "r", "l", "b", "d"]
        for letter in letters:
            inverse_letter = str.swapcase(letter)
            moves = moves\
                .replace(letter * 3, inverse_letter)\
                .replace(inverse_letter * 3, letter)\
                .replace(letter + inverse_letter, "")\
                .replace(inverse_letter + letter, "")
        return moves

    def locate_match(self, candidates, current_face, reference_block):
        """ This function is concerned with picking out the component that exactly matches the one we're looking to insert.
            current_face: the current orientation from which we're visualizing the cube, needed to make sure we get the right index.
            reference_face: the block we're comparing against and trying to find a solution for
        """
        # List out candidates and index them
        for x, candidate in enumerate(candidates):
            
            # Locate candidates based on adjacency matching on the same face
            if current_face.adjacencies == candidate.adjacent_faces:
                
                # Attempt to find candidates that match a success metric value first, before picking the alternative candidate
                try:
                    bottomindex = list(self.value.success_metric).index(candidate.arrangement)
                    return bottomindex, candidate
                except ValueError:
                    pass
                return x, candidate
        else:
            # This indicates this face is already solved as there is no candidate
            return -1, None

    @staticmethod
    def translate_heuristics(heuristics, face, adjustment_rotations):
        """ Receives in a series of heuristics and applies transformations in context of a target face.
            It also applies a series of adjustment rotations to each heuristic if several must be tested to find the correct one.
        """
        transformed_heuristics = []
        for heuristic in heuristics:
            
            # Add each value in the adjustment patterns group to the beginning of each of the algorithms
            for adjustment_pattern in adjustment_rotations:
                new_heuristic = ''
                
                # Ensure that both the adjustment pattern and the heuristic both get translations applied to them
                for command in (adjustment_pattern + heuristic):
                    translated_heuristic = CubeFace.translate_rotation(command, face)
                    
                    # Determine direction by upper/lowercase ascii value
                    if ord(command) >= 97:
                        translated_heuristic = translated_heuristic.lower()
                    new_heuristic += translated_heuristic
                
                # Add transformed and padded heuristic back to list
                transformed_heuristics.append(new_heuristic)
        return transformed_heuristics

    def get_pieces_solved(self, faces, pieces):
        """ Ensures that for a given phase, all piece types matching a face or group of faces match 
            the expected values to verify the phase solution. 
        """
        if self.name == 'BottomCross':
            return list(
                filter(
                    lambda v:
                        v.value == faces.D.center.value and v.arrangement.piece_type == 'EDGE',
                        pieces[45:53]
                )
            ).__len__()
        elif self.name == "LowerLayer":
            return list(
                filter(
                    lambda v:
                        v.value == faces.D.center.value and v.arrangement.piece_type == 'CORNER',
                        pieces[45:54]
                )
            ).__len__()

    def get_candidates(self, faces, pieces):
        """ Obtain all possible piece candidates for insertion in no particular order.
            This function takes an array of faces and pieces to find pieces of the same color, orientation, and type.
            Functionality can be overridden based on the current phase for maximum flexibility
        """
        possibilities = []
        if self.name == 'BottomCross':
            preliminary = CubeArrangement.get_cohesive_pieces(
                pieces,
                faces.D.center.value,
                PieceType.EDGE
            )

            # Eliminate pieces that are already set
            for possibility in preliminary:
                if possibility.adjacent_faces == possibility.arrangement.adjacencies:
                    # If on piece 45 and above (bottom of the cube), skip unless stem doesn't match and recalculation is needed
                    if possibility.index >= 45:
                        continue
                possibilities.append(possibility)
        elif self.name == 'LowerLayer':
            possibilities = CubeArrangement.get_cohesive_pieces(
                pieces,
                faces.D.center.value,
                PieceType.CORNER
            )
        return possibilities


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
    current_face: int
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

    def rotate(self, pieces, command):
        """ Allows rotation of a single face in a clockwise or anti-clockwise direction. """
        # Determine direction by upper/lowercase ascii value
        direction = "CW"
        if ord(command) >= 97:
            direction = "ACW"

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
        """ This mapping is made to allow the cube to be solved from the same initial point regardless of the perspective from which the cube
            is being solved. This allows a dramatic cutdown of the amount of algorithms required to represent cube solutions.
        """
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
            }[rotation.upper()]
        elif destination_face == 2:
            return {
                "F": "B",
                "R": "L",
                "B": "F",
                "L": "R",
                "U": "U",
                "D": "D"
            }[rotation.upper()]
        elif destination_face == 3:
            return {
                "F": "L",
                "R": "F",
                "B": "R",
                "L": "B",
                "U": "U",
                "D": "D"
            }[rotation.upper()]
        elif destination_face == 4:
            return {
                "F": "U",
                "R": "R",
                "B": "D",
                "L": "L",
                "U": "B",
                "D": "F"
            }[rotation.upper()]
        elif destination_face == 5:
            return {
                "F": "D",
                "R": "R",
                "B": "U",
                "L": "L",
                "U": "F",
                "D": "B"
            }[rotation.upper()]


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
        """ This process reads in a cube string and unpacks each value to create cube pieces to add to a cube. """
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
                current_face=x // CUBE_FACE_PIECES,
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
        """ Updates internal state to recalculate cube mappings and locations. """
        # Retrieve pinned centerpieces by location
        for x, i in enumerate(range(4, 53, 9)):
            self._pinned_centerpieces[self._cube_string[i]] = x

        # Test for non-unique centerpieces
        if self._pinned_centerpieces.__len__() != CUBE_FACES:
            raise InvalidCubeCenter(self)

        # Handle error case where invalid centers would trigger a KeyError on previous assignments
        try:
            self._cube_map = [self._pinned_centerpieces[face] for face in self._cube_string]
        except KeyError:
            raise InvalidCubeCenter(self)

    def _add_piece(self, piece: CubePiece):
        """ Add a single piece to a cube representation. At most 54 pieces may be added.
            Checks to make sure that the piece is valid in context with the previously added pieces,
            and ensures that the piece types get updated as new pieces are added.
        """
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
        """ Calculate faces, corners, and edges for a cube. """
        for i in range(0, CUBE_FACES):
            # Obtain centerpiece, edges, and corners
            self._faces(i).center = CubeArrangement.get_face_pieces(self._pieces, i, PieceType.CENTER)[0]
            self._faces(i).edges = CubeArrangement.get_face_pieces(self._pieces, i, PieceType.EDGE)
            self._faces(i).corners = CubeArrangement.get_face_pieces(self._pieces, i, PieceType.CORNER)

    def rotate(self, rotate_command: List[str] = None):
        """ Performs cube rotations from a command list, reconstructing/rebuilding after each execution phase and appending to global state. """
        # Iterate through rotation commands, updating state each time
        for command in rotate_command:
            # Perform in-place rotation within face
            self._faces[command.upper()].rotate(self._pieces, command)

            # Save states to be able to show stages along with final results
            self._reconstruct()
            self._state.append(self._cube_string)

    def solve(self, cube_phase=10):
        """ This method executes a cube solve up to a certain operation phase.
            It locates the candidates, queries the algorithm class, performs the prescribed rotations, and checks if output was successful.
        """
        # First step is to check if the cube is already solved, if so, return an empty string
        last = self._cube_map[0]
        for new_last in self._cube_map[1:54]:
            if last > new_last:
                break
            last = new_last
        else:
            return ""
        
        # Target a specific solve step or a series of steps
        # heuristic_phases = [CubeHeuristics.BottomCross, CubeHeuristics.LowerLayer]
        heuristic_phases = [CubeHeuristics.BottomCross]

        # Check if we qualify for a bottom cross
        centerpiece = self._faces.D.center

        # Show original cube to compare against final iteration
        original_cube = "".join([f.value for f in self._pieces])
        print(f'Original cube: \n{original_cube}')

        # Store a list of all rotations for this cube
        final_rotations = ''

        # Run once for as many heuristic phases as we have. Phases that show completion should be skipped
        for heuristic in heuristic_phases:
            
            # Leave headroom for unsolved pieces when operations require multiple laps
            remaining_iterations = 1
            unsolved_pieces = True
            
            # Candidates are read on every loop, some heuristics require multiple passes
            while unsolved_pieces:
                
                # Apply rotations and append to rotation list if any were found
                final_rotations += self._attempt_algorithms(heuristic, centerpiece)

                # Check if all pieces have been solved for current phase (TODO: in the future, run all verifications in series to make sure a step hasn't broken another)
                if heuristic.get_pieces_solved(self._faces, self._pieces) == 4:
                    unsolved_pieces = False
                elif remaining_iterations <= 0:
                    # If we have exceeded the number of iteration steps, the cube may be invalid (tampered) or we have an edge case to consider
                    raise TamperedCube(self)
                remaining_iterations -= 1

            # Visually verify solutions
            print(f'\nNew cube: \t\t{self._cube_string}')

            # Return final rotation
            print(f'Rotations: \t\t{final_rotations}\n')
        return final_rotations
    
    
    def _attempt_algorithms(self, heuristic, centerpiece):
        # Parse through candidates to find best match
        new_rotations = ''
        for current_face in [0, 1, 2, 3]:
            
            # Identify candidates for current heuristic phase
            candidates = heuristic.get_candidates(self._faces, self._pieces)
            
            # If we have not found any candidates, this face is solved
            if not candidates:
                break
            
            # Identify algorith or heuristic leading to a solution
            algorithm, success_condition = heuristic.get_algorithm_by_arrangement(candidates, current_face, centerpiece.adjacent_faces)

            # Test potential solutions from returned algorithms
            for heuristic_algorithm in algorithm:
                
                # Perform and apply individual rotations and update state list, then rebuild cube mappings
                for command in heuristic_algorithm:
                    self._faces[command.upper()].rotate(self._pieces, command)
                    tentative = ("".join([f.value for f in self._pieces]))
                    self._state.append(tentative)
                self._reconstruct()


                # Check for success by comparing block against success condition and passthrough transition steps
                if success_condition is None or self._heuristic_success(success_condition):
                    new_rotations += heuristic_algorithm
                    break

                # Undo operations by reversing heuristic steps and applying the inverse steps, then rebuild cube mappings
                for command in reversed(heuristic_algorithm.swapcase()):
                    self._faces[command.upper()].rotate(self._pieces, command)
                    self._state.pop()
                self._reconstruct()
        
        # Return newly identified rotations or an empty string if there are none
        return new_rotations
    
    def _heuristic_success(self, success_condition):
        """ Verify that heuristic success condition is true by checking predicted adjacencies vs actual adjacencies """
        return list(success_condition.adjacencies) == sorted([self._cube_map[piece] for piece in success_condition.true_indexes])

    def _reconstruct(self):
        """ Update cube string by appending all cube values in order to a string to save state, and remap (this is useful in case a center turn is ever added). """
        self._cube_string = "".join([f.value for f in self._pieces])
        self._remap_pieces()
        new_adjacencies = [{self._cube_map[face] for face in piece.arrangement.true_indexes} for piece in self._pieces]
        for x in range(0, len(self._pieces)):
            self._pieces[x].adjacent_faces = new_adjacencies[x]

    def __str__(self):
        return self._cube_string

    def __repr__(self):
        return f'{self._cube_string}\n{self._cube_map}'
