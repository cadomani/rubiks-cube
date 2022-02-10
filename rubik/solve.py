import rubik.cube as rubik
import re
from rubik.utils.exceptions import SolveError, CubeError, InvalidRotateCommand

VALID_ROTATIONS_REGEX = r"[frblud]"
    
    
def _solve(parms):
    # Pull both required parameters
    cube = parms.get('cube')
    rotate_command = parms.get('rotate')

    try:
        # Pass valid rotation if it is empty
        if rotate_command is None or rotate_command == '':
            rotate_command = "F"

        # Return a standardized copy of the rotate command if it contains 'Tt' and 'Uu' references. Only match in the presence of a 'Tt'
        if 't' in rotate_command or 'T' in rotate_command:
            rotate_command = rotate_command.replace('u', 'd').replace('U', 'D').replace('T', 'U').replace('t', 'u')

        # Match valid characters
        rotations = re.findall(VALID_ROTATIONS_REGEX, rotate_command, re.IGNORECASE)
        if len(rotations) != len(rotate_command):
            raise InvalidRotateCommand(cube, rotate_command)

        # Pass cube and rotations array to cube class for processing
        cube = rubik.Cube(input_cube=cube)

        # Rotate cube by command
        cube.rotate(rotate_command)
    except (SolveError, CubeError) as e:
        return {"status": str(e)}
    except Exception as e:
        # Catch all other exceptions not handled above
        return {"status": f"error: an exception occurred - {str(e)}"}
    return {"status": "ok", "cube": str(cube)}
