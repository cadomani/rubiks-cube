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
        """ Checking behavior is necessary so this test does not fail. In this case, check that all values are contiguous and serialized. """
        parm = {
            'op'    : 'solve',
            'cube'  : 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
        }
        expected = {
            'status': 'ok',
            'solution'  : '',
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        rotations = result.get('solution', None)
        self.assertEqual(expected['solution'], rotations)

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

    # @unittest.skip("Need to do some work to ensure a single rotation is detected and all other phases detect completion, but that requires all phases to be done")
    def test_solve_040_ShouldReturnSingleRotationOnSolveRequest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '005005005111111111422422422333333333440440440552552552',
        }
        expected = {
            'status': 'ok',
            'solution': 'r'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)
        
    # @unittest.skip("Need to do some work to ensure a single rotation is detected and all other phases detect completion, but that requires all phases to be done")
    def test_solve_041_ShouldReturnSingleRotationOnSolveRequest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '004004004111111111522522522333333333442442442550550550',
        }
        expected = {
            'status': 'ok',
            'solution': 'R'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    # @unittest.skip("skip to ensure non-edge cases pass first")
    def test_solve_042_ShouldSolveMiddleLayer(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '443303302550412532534424421302132022001141100551555413',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'UFrfLLUBBlRUrUrURFUfubUBlULuufuFBUburuRLUlubuBFUfuluL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    def test_solve_043_ShouldSolveMiddleLayer(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '440502105425110222255123152041431410301045023533453334',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'UrFFrFFUUBBBlFbubuBBUbUUFUUfUFufuufuFuurURLUlubuBFUfuluL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    def test_solve_044_ShouldSolveMiddleLayer(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '105302150312115455333021045054432325444140232221453001',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'RRFUbRlUBBUBlbFUfuufuFUrURFUfbuBUlUL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    # @unittest.skip("skip to ensure non-edge cases pass first")
    def test_solve_045_ShouldSolveMiddleLayer(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '232502120330412143401523505411433315043540424215051052',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'BBUUFFRRLUlBBluufuFLUlurURLUluubUBuluL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    def test_solve_046_ShouldSolveMiddleLayer(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '004104055235214354211124052241030351421342533410352503',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'frbLbuBLLFFuruRFUfubUBuFUUfUFufuRUUrURurBUburuRLUlubuBFUfuluL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    def test_solve_047_ShouldSolveMiddleLayer(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '510400103321113412401224421522330430230441345550555253',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'FUfuufuFUrURFUfbuBUlUL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # rotations = result.get('solution', None)
        # self.assertEqual(expected['solution'], rotations)

    def test_solve_048_ShouldSolveMiddleLayerWithCrossMissedFromA4Grade(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'CggCggCggzrrzrrzrrgCCgCCgCCzzrzzrzzrL333L3L333LLL3L3LL',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'FFRRBBLLRUrufuFUbUBuuluLRUrufuFurURLUlubuBFUfuluL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

    def test_solve_049_ShouldSolveMiddleLayerWithBottomLayerMissedFromA5Grade(self):
        parm = {
            'op'    : 'solve',
            'cube'  : 'qtDDttTtTqqDqTDDTLLTLTLtfLTfLtDqLfqDqLqqDDfTttfLffftfT',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'LUlfUFBUbuurURLUlubuBluL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

    def test_solve_050_ShouldSolveMiddleLayerFromStressTest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '425000121003511454412422033121534540552441013532353203',
        }
        expected = {
            'status': 'ok',
            # 'solution': 'FURRBUfLFuRUUrURurruRubUBUlUL'
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

    def test_solve_051_ShouldSolveMiddleLayerFromStressTest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '210505201400310003523121252535232334041445143134254514',
        }
        expected = {
            'status': 'ok',
            # 'solution': ''
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

    # @unittest.skip("skip to ensure non-edge cases pass first")
    def test_solve_052_ShouldSolveMiddleLayerFromStressTest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '201502033253411543501221234005533011530542114422450344',
        }
        expected = {
            'status': 'ok',
            # 'solution': ''
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

    def test_solve_053_ShouldSolveMiddleLayerFromStressTest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '405102322351310550201121440033435520554443232441152301',
        }
        expected = {
            'status': 'ok',
            # 'solution': ''
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

    def test_solve_054_ShouldSolveMiddleLayerFromStressTest(self):
        parm = {
            'op'    : 'solve',
            'cube'  : '130304510540213554104025354322032203044143551243151122',
        }
        expected = {
            'status': 'ok',
            # 'solution': ''
        }
        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # solution = result.get('solution', None)
        # self.assertEqual(expected['solution'], solution)

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

    def test_solve_940_ShouldReturnProperlyFormattedErrorString(self):
        """ This test case was derived upon review to address a formatting issue causing failed tests. Matches a3_930. """
        parm = {
            'op'    : 'solve',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwwe',
            'rotate': 'F'
        }
        expected = {
            'status': 'error: invalid cube configuration - the cube does not contain six unique center pieces'
        }

        result = solve._solve(parm)
        status = result.get('status', None)
        self.assertEqual(expected['status'], status)

        # Verify that we have not sent a cube parameter on a failure case
        self.assertNotIn('cube', result)

