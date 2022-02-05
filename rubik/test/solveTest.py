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

    def test_solve_010_ShouldReturnOkOnValidRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
            'rotate': 'F'
        }
        expected = {
            'status': 'ok'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

    # @unittest.skip()
    # def test_solve_050_ShouldReturnOkOnValidRotation(self):
    #     parm = {
    #         'op': 'solve',
    #         'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
    #         'rotate': 'F'
    #     }
    #     expected = {
    #         'status': 'ok',
    #         'cube': 'bbbbbbbbbyrryrryrrgggggggggoowoowoowyyyyyyooorrrwwwwww',
    #     }
    #     result = solve._solve(parm)
    #     status = result.get('status', None)
    #     self.assertEqual(expected['status'], status)
    #
    #     cube = result.get('cube', None)
    #     self.assertEqual(expected['cube'], cube)

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
