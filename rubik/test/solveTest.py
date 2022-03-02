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

    # --------------------------------------------------------
    # HAPPY PATH TESTS
    # --------------------------------------------------------

    def test_solve_010_ShouldReturnSolutionOnMissingRotateParameter(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
        }
        expected = {
            'status': 'ok',
            'rotations'  : '',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        rotations = result.get('rotations', None)
        self.assertEqual(expected['rotations'], rotations)

    def test_solve_011_ShouldReturnFrontRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy',
            'rotate': 'F'
        }
        expected = {
            'status': 'ok',
            'cube'  : 'gggggggggwrrwrrwrrbbbbbbbbbooyooyooywwwwwwooorrryyyyyy',
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

    def test_solve_021_ShouldReturnCubeOnSimpleRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy',
            'rotate': 'R'
        }
        expected = {
            'status': 'ok',
            'cube'  : 'ggyggyggyrrrrrrrrrwbbwbbwbbooooooooowwgwwgwwgyybyybyyb',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)
        
    def test_solve_022_ShouldReturnCubeOnSimpleRotation(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy',
            'rotate': 'B'
        }
        expected = {
            'status': 'ok',
            'cube'  : 'gggggggggrryrryrrybbbbbbbbbwoowoowoorrrwwwwwwyyyyyyooo',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    def test_solve_023_ShouldReturnCubeOnOnSimpleRotations(self):
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

    def test_solve_024_ShouldReturnCubeOnOnSimpleRotations(self):
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

    def test_solve_025_ShouldReturnOriginalCubeOnReturnToHomeRotation(self):
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

    def test_solve_026_ShouldReturnOriginalCubeOnReturnToHomeRotation(self):
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

    def test_solve_027_ShouldReturnOriginalCubeOnReturnToHomeRotation(self):
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

    def test_solve_028_ShouldReturnOriginalCubeOnReturnToHomeAlgorithm(self):
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

    def test_solve_030_ShouldReturnKnownScrambledCube(self):
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

    def test_solve_031_ShouldReturnKnownSolvedCube(self):
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
        
    # @unittest.skip('invalid rotation parameters given: "Tt"')
    def test_solve_032_ShouldReturnKnownSolvedCube(self):
        """ This test includes a non-standard rotate parameter where T and t indicate U and u respectively, and U and u indicate D and d.
            Unfortunately, there isn't a way to know for certain that a U or u without the presence of a D or T belongs to one or the other group.
            Assume that a customer that uses a T is using T/U notation, and a customer using a D/U or U only is using the standard D/U notation.
        """
        parm = {
            'op'    : 'solve',
            'cube'  : 'rbbgbobbgrgwyrywyobggrggywgoryyowowwyoobyrgwyrorrwbwob',
            'rotate': 'FLFFBTTuLfUrFLuRRuLLuRRt'
        }
        expected = {
            'status': 'ok',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)

    # --------------------------------------------------------
    # SINGLE MOVE SOLUTIONS
    # --------------------------------------------------------
    
    def test_solve_040_ShouldReturnSingleRotationOnSolveRequest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '005005005111111111422422422333333333440440440552552552',
        }
        expected = {
            'status': 'ok',
            'rotations': 'r'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        rotations = result.get('rotations', None)
        self.assertEqual(expected['rotations'], rotations)
        
    def test_solve_041_ShouldReturnSingleRotationOnSolveRequest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '004004004111111111522522522333333333442442442550550550',
        }
        expected = {
            'status': 'ok',
            'rotations': 'R'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        rotations = result.get('rotations', None)
        self.assertEqual(expected['rotations'], rotations)

    def test_solve_042_ShouldSolveComplexLastCrossPiece(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '443303302550412532534424421302132022001141100551555413',
        }
        expected = {
            'status': 'ok',
            'rotations': 'Rbr'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        rotations = result.get('rotations', None)
        self.assertEqual(expected['rotations'], rotations)
        
    def test_solve_043_ShouldSolveComplexLastCrossPiece(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '334002333032410411312322205415134055104444221050255155',
        }
        expected = {
            'status': 'ok',
            'rotations': 'LdB'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        rotations = result.get('rotations', None)
        self.assertEqual(expected['rotations'], rotations)


    # --------------------------------------------------------
    # SAD PATH TESTS
    # --------------------------------------------------------
    
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
        
    def test_solve_921_ShouldReturnErrorOnMissingCube(self):
        parm = {
            'op'    : 'solve',
            'rotate': 'F',
            'cube': None
        }
        expected = {
            'status': 'error: the cube parameter is missing'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)
        
    def test_solve_922_ShouldReturnErrorOnMissingCube(self):
        parm = {
            'op'    : 'solve',
            'rotate': 'F',
            'cube': ''
        }
        expected = {
            'status': 'error: the cube parameter is missing'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)

