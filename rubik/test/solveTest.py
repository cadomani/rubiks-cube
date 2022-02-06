from unittest import TestCase
import rubik.solve as solve
import unittest


class SolveTest(TestCase):
    """
        Tests should be created in the order they should be processed in, to avoid working on tests that
        do a lot of heavy lifting very early on (e.g. tests with full rotations before input validation is done)
        
        Here, it makes more sense to write sad path tests first, to get validation done so that happy path issues
        don't encounter issues where the happy path tests fail due to lack of validation instead of failing due to
        the expected results not being matched.            
    
    """
    # @unittest.skip('need mixed cube to test distinct faces')
    def test_solve_010_ShouldReturnOkOnValidFaceRotation(self):
        parm = {
            'op': 'solve',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
            'rotate': 'F'
        }
        expected = {
            'status': 'ok',
            'cube': 'bbbbbbbbbyrryrryrrgggggggggoowoowoowyyyyyyooorrrwwwwww',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)
    
        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    # @unittest.skip('face rotation tested, need to test simple skirt rotation')
    def test_solve_020_ShouldReturnOkOnValidRotation(self):
        # Incomplete test with invalid edge and corner solutions, but face values are correct
        parm = {
            'op'    : 'solve',
            'cube'  : 'rooywowobbgwbbowbyoryyywowybbwrgrgygrbgworbwyrgogryrgg',
            'rotate': 'F'
        }
        expected = {
            'status': 'ok',
            'cube'  : 'wyrowoboobgwbbowbyoryyywowybbwrgrgygrbgworbwyrgogryrgg',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_910_ShouldReturnErrorOnInvalidRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
            'rotate': 'm'
        }
        expected = {
            'status': 'error: the rotate command is invalid'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)
        
    def test_solve_911_ShouldReturnErrorOnMissingRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww'
        }
        expected = {
            'status': 'error: the rotate command is missing'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)
    
    def test_solve_920_ShouldReturnErrorOnMissingCube(self):
        parm = {
            'op'    : 'solve',
            'rotate': 'F'
        }
        expected = {
            'status': 'error: the cube parameter is missing'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)
        
    def test_solve_930_ShouldReturnErrorOnMissingParameters(self):
        parm = {
            'op'    : 'solve',
        }
        expected = {
            'status': 'error: both a cube and a rotation parameter must be provided'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)

