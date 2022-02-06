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
    try:
        _ = rubik.Cube(parms.get('cube'))
    except CubeError as e:
        return {'status': str(e)}
    except Exception as e:
        # Catch all other exceptions not handled above
        return {"status": f"error: an exception occurred - {str(e)}"}
    return {'status': 'ok'}
