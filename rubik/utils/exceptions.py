class CubeError(BaseException):
    """ Base exception for the cube check operation. """
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
    def __init__(self, piece_face, problem_cube):
        super().__init__(f'error: the "{piece_face}" face value does not occur 9 times', problem_cube)


class InvalidCubeDeclaration(CubeError):
    """ Base exception for any cube declaration issues. """
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


class SolveError(BaseException):
    """ Base exception for the cube solve operation. """
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


class InvalidRotateCommand(SolveError):
    def __init__(self, problem_cube, rotate_command):
        super().__init__("error: the rotate command is invalid", problem_cube, rotate_command)