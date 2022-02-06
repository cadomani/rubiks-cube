import rubik.solve as solve
import unittest


class SolveTest(unittest.TestCase):
    """
        Tests should be created in the order they should be processed in, to avoid working on tests that
        do a lot of heavy lifting very early on (e.g. tests with full rotations before input validation is done)
        
        Here, it makes more sense to write sad path tests first, to get validation done so that happy path issues
        don't encounter issues where the happy path tests fail due to lack of validation instead of failing due to
        the expected results not being matched.            
    
    """

    def test_solve_010_ShouldReturnFrontRotationOnMissingRotateParameter(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
        }
        expected = {
            'status': 'ok',
            'cube'  : 'bbbbbbbbbyrryrryrrgggggggggoowoowoowyyyyyyooorrrwwwwww',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_020_ShouldReturnCubeOnSimpleRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '544204041130114012542220402110535323513045102534352533',
            'rotate': 'F'
        }
        expected = {
            'status': 'ok',
            'cube'  : '025404144130014212542220402115533324513045350011352533',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_030_ShouldReturnCubeOnOnSimpleRotations(self):
        """ Test with clockwise rotations only """
        parm = {
            'op'    : 'solve',
            'cube'  : '000000000111111111222222222333333333444444444555555555',
            'rotate': 'RULBFD'
        }
        expected = {
            'status': 'ok',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_031_ShouldReturnCubeOnOnSimpleRotations(self):
        """ Test with clockwise rotations only """
        parm = {
            'op'    : 'solve',
            'cube'  : '000000000111111111222222222333333333444444444555555555',
            'rotate': 'rulbfd'
        }
        expected = {
            'status': 'ok',
            'cube'  : '344300212003512155442122030134534555522044011304351321',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_040_ShouldReturnOriginalCubeOnReturnToHomeRotation(self):
        """ Test and undo moves to validate robustness. """
        parm = {
            'op'    : 'solve',
            'cube'  : '000000000111111111222222222333333333444444444555555555',
            'rotate': 'RrUuLlBbFfDd'
        }
        expected = {
            'status': 'ok',
            'cube'  : '000000000111111111222222222333333333444444444555555555',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_041_ShouldReturnOriginalCubeOnReturnToHomeRotation(self):
        """ Test and undo moves to validate robustness. """
        parm = {
            'op'    : 'solve',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
            'rotate': 'BbFfDdRrUuLl'
        }
        expected = {
            'status': 'ok',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_042_ShouldReturnOriginalCubeOnReturnToHomeRotation(self):
        """ Test and undo moves to validate robustness. """
        parm = {
            'op'    : 'solve',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
            'rotate': 'ddddDDDDuuuuUUUUffffFFFFbbbbBBBBllllLLLLrrrrRRRR'
        }
        expected = {
            'status': 'ok',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_050_ShouldReturnOriginalCubeOnReturnToHomeAlgorithm(self):
        """ Test and undo moves to validate robustness. """
        parm = {
            'op'    : 'solve',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
            'rotate': 'rdRDrdRDrdRDrdRDrdRDrdRD'
        }
        expected = {
            'status': 'ok',
            'cube'  : '044001232322015551443223010431435555211244500301351324',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_060_ShouldReturnKnownScrambledCube(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '000000000111111111222222222333333333444444444555555555',
            'rotate': 'DDRRdfblbLfDDFrBBdlbUUFFlRfUUbLLR'
        }
        expected = {
            'status': 'ok',
            'cube'  : '425100353215413244324524020151135105232040011024353543',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_070_ShouldReturnKnownSolvedCube(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '425100353215413244324524020151135105232040011024353543',
            'rotate': 'rllBuuFrLffuuBLDbbRfddFlBLBFDrrdd'
        }
        expected = {
            'status': 'ok',
            'cube'  : '000000000111111111222222222333333333444444444555555555',
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

    def test_solve_911_ShouldReturnErrorOnInvalidRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
            'rotate': 'Bmyrb'
        }
        expected = {
            'status': 'error: the rotate command is invalid'
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
