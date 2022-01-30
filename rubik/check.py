import rubik.cube as rubik
from rubik.cube import CubeError


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
    # Instead of returning a dictionary with keys, we early return in every function to short-circuit and avoid extra work
    try:
        cube_str = parms['cube']
        _ = rubik.Cube(cube_str)
    except CubeError as e:
        return {'status': str(e)}
    except KeyError:
        return {'status': 'error: the cube parameter is missing'}
    else:
        # If no errors occurred, return ok.
        return {'status': 'ok'}
