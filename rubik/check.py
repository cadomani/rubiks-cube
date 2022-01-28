import rubik.cube as rubik
import re

# CORNERS = [1, 3, 7, 9]
# CENTER = 5
# LIASONS = [
#     (2, 2),
#     (2, 8),
#     (4, 6),
#     (6, 4),
#     (8, 2),
#     (8, 8)
# ]


def _check(parms):
    """ Quality checks the input key-value pairs, particularly 'cube'

        Success status returned if the value of 'cube':
           is valid
           is a string
           has 54 elements
           has 9 occurrences of 6 colors
           has each middle face being a different color

        Otherwise, we return the relevant error

        EC:
            Find out if cube contains contradictory colors

        @return dict: {'status': 'ok'} or {'status': 'error: xxx'}
    """
    # Test to see if cube value is included in parameters
    try:
        cube = parms['cube']
    except KeyError:
        return {'status': 'error: the cube parameter is missing'}

    # Test to see if value is a string
    if not isinstance(cube, str):
        return {'status': 'error: the cube value is not a string'}

    # Test for the value length
    if not len(cube) == 54:
        return {'status': 'error: the cube is not 54 characters in length'}

    # Check for illegal characters. Match 54 characters containing a-z, A-Z, and 0-9 only. No match returns None.
    if not re.match(r'[a-zA-Z0-9]{54}', cube):
        return {'status': 'error: the cube contains invalid characters'}

    # Consume input into parts to test each status and test middle face of each
    included = {}
    center_values = set()
    for x, value in enumerate(cube):
        # Instead of a 4-line if statement, we take advantage of the dictionary's get method to return a value of 0 if the key does not exist and add one to increment
        included[value] = included.get(value, 0) + 1

        # In the same loop, we collect the modulo 9 of each key and store the 5th one coinciding with the center element
        if (x + 1) % 9 == 5:
            center_values.add(value)

    # We enumerate through the dictionary we created before and check that every key occurs exactly 9 times, this has the side effect of checking that values are unique too
    for color, incidence in included.items():
        if incidence != 9:
            return {'status': f'error: the "{color}" face does not occur 9 times'}

    # Test if we had 6 unique center values. The overall 6 total values are mathematically validated above so this is a redundancy.
    if len(center_values) != 6:
        return {'status': 'error: invalid arrangement of center pieces'}

    # EC: Verify that the positioning of the elements in the cube is valid by
    if not _is_valid_arrangement(cube, center_values):
        return {'status': 'error: invalid cube arrangement'}

    # If no errors occurred, return ok. Instead of returning a dictionary with keys, we early return in every function to short-circuit and avoid extra work
    return {'status': 'ok'}


def _is_valid_arrangement(cube, center_values):
    """ Test to see if a partially-solved cube has invalid positions.

        Algorithm:
        1. Identify centerpoints and iterate through them
        2. Identify centerpoint face pieces and corner elements
        3. Identify centerpoint facce corner elements and the boundary pieces
        4. Locate centerpoint and opposing face color.
        5. If face color matches corner elements, it is invalid
    """
    # Enumeration for pieces in order F, R, B, L, U, B
    for x, primary_piece in enumerate(center_values):
        # Define boundaries
        boundary_start = x * 9
        # boundary_end = boundary_start + 8

        # Corner elements and opposing pieces
        corner_elements = None
        opposing_centerpiece = None

        # Choose element indexes by the face value
        if x == 0:
            # Front face
            corner_elements = [(1, 30, 43), (3, 10, 45), (7, 36, 46), (9, 16, 48)]
            opposing_centerpiece = 22
        elif x == 1:
            # Right face
            corner_elements = [(3, 10, 45), (12, 19, 39), (9, 16, 48), (18, 25, 54)]
            opposing_centerpiece = 31
        elif x == 2:
            # Blue face
            corner_elements = [(12, 19, 39), (21, 28, 37), (18, 25, 54), (27, 34, 52)]
            opposing_centerpiece = 4
        elif x == 3:
            # Left face
            corner_elements = [(21, 28, 37), (1, 30, 43), (27, 34, 52), (7, 36, 46)]
            opposing_centerpiece = 13
        elif x == 4:
            # Upper face
            corner_elements = [(21, 28, 37), (12, 19, 39), (1, 30, 43), (3, 10, 45)]
            opposing_centerpiece = 49
        elif x == 5:
            # Bottom face
            corner_elements = [(7, 36, 46), (9, 16, 48), (27, 34, 52), (18, 25, 54)]
            opposing_centerpiece = 40

        valid = _valid_solved_face_boundaries(
            cube[boundary_start + 4],
            _corner_indexes_to_values(cube, corner_elements),
            cube[opposing_centerpiece]
        )
        if not valid:
            return False
    return True


def _corner_indexes_to_values(cube, corners):
    """ Obtain cube values from respective cube indexes. """
    new_corners = []
    for corner in corners:
        corner_values = []
        for value in corner:
            corner_values.append(cube[value - 1])
        new_corners.append(corner_values)
    return new_corners


# # NOT YET USED
# def _contiguous_faces(cube):
#     """ Asserts that each cube face is a unique combination of colors (solved). """
#     for face in range(0, 6):
#         face_color = None
#         for index in range(0, 9):
#             cube_index = _to_cube_index(face, index)
#             if not face_color:
#                 face_color = cube[cube_index]
#             else:
#                 if cube[cube_index] != face_color:
#                     return False
#     return True
#
#
# # NOT YET USED
# def _to_row_major(cube_index):
#     """ Return the value as an index from 1 to 9. """
#     return 9 if cube_index % 9 == 0 else cube_index % 9
#
#
# # NOT YET USED
# def _to_cube_index(face_index, row_major_value):
#     """ Return the value as a cube index from 1 to 54. """
#     return (face_index * 9) + row_major_value
#
#
# # NOT YET USED
# def _pin_corners(cube):
#     """ Assert that the corners tied to the front face are valid, pinning them and validating the rest of the cube as a side effect. """
#     pass


def _valid_solved_face_boundaries(primary_piece, corner_pieces, opposite_piece):
    """ Assert that a single corner of the cube is valid given its positioning.

        Key:
        Any corners containing the same value as the primary piece should not have any values th
        are the same as the opposite piece.
    """
    for corner in corner_pieces:
        for value in corner:
            # The secondary check is expensive, but due to short-circuiting,
            # it does not get evaluated unless the more rare condition (placed first) is true
            if value == opposite_piece and primary_piece in corner:
                return False
    return True
