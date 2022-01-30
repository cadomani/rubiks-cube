from unittest import TestCase
import rubik.check as check


class CheckTest(TestCase):
    def test_check_010_ShouldReturnOkOnSolvedCube(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_020_ShouldReturnOkOnAlphanumericInput(self):
        parm = {
            'op': 'check',
            'cube': '999999999777777777111111111rrrrrrrrrgggggggggmmmmmmmmm'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_030_ShouldReturnOkOnMixedCaseAlphanumeric(self):
        parm = {
            'op': 'check',
            'cube': '999999999777777777888888888RRRRRRRRRooooooooonnnnnnnnn'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_040_ShouldReturnOkOnMixedCaseAlphabeticalWithSameLetters(self):
        parm = {
            'op': 'check',
            'cube': 'lllllllllLLLLLLLLLoooooooooOOOOOOOOOPPPPPPPPPppppppppp'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_050_ShouldReturnOkOnNumerical(self):
        parm = {
            'op': 'check',
            'cube': '999999999777777777111111111888888888666666666444444444'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_060_ShouldReturnOkOnNonStandardArrangementOfCornerPieces(self):
        # This test is set to match a similar arrangement to EC, but it is perfectly solvable
        # due to the relevant face pieces not being contiguous yet
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggooooooooowyyyyyyyyywwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_070_ShouldReturnOkOnScrambledCube(self):
        parm = {
            'op': 'check',
            'cube': 'rooywowobbgwbbowbyoryyywowybbwrgrgygrbgworbwyrgogryrgg'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_071_ShouldReturnOkOnScrambledCube(self):
        parm = {
            'op': 'check',
            'cube': '544204041130114012452220402110535323513045102534352533'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_072_ShouldReturnOkOnScrambledCube(self):
        parm = {
            'op': 'check',
            'cube': 'OBRRBBBGWGBRWWRRGOYGWYGWGYBRGWOYBOROBOBYRYGOYWWGWORYOY'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)

    def test_check_910_ShouldReturnErrorOnMissingCube(self):
        parm = {
            'op': 'check'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: the cube parameter is missing', status)

    def test_check_911_ShouldReturnErrorOnInvalidCubeType(self):
        parm = {
            'op': 'check',
            'cube': 999999999777777777111111111888888888666666666444444444
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube declaration - the cube value is not a string', status)

    def test_check_912_ShouldReturnErrorOnNullCubeType(self):
        parm = {
            'op': 'check',
            'cube': None
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: the cube parameter is missing', status)

    def test_check_920_ShouldReturnErrorOnCubeOverLength(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube declaration - the cube is not 54 characters in length', status)

    def test_check_921_ShouldReturnErrorOnCubeUnderLength(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrggggggggoooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube declaration - the cube is not 54 characters in length', status)

    def test_check_930_ShouldReturnErrorOnInvalidCharacters(self):
        parm = {
            'op': 'check',
            'cube': '%%%%%%%%%777777777.........RRRRRRRRR[[[[[[[[[MMMMMMMMM'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube declaration - the cube contains invalid characters', status)

    def test_check_931_ShouldReturnErrorOnInvalidCharacters(self):
        # Pass in what should be a raw string without prepending 'r' to make sure that backslashes don't get skipped or misinterpreted on regex
        parm = {
            'op': 'check',
            'cube': r'\.\.\.\.\\.\.\.\.\\.\.\.\.\\.\.\.\.\\.\.\.\.\\.\.\.\..'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube declaration - the cube contains invalid characters', status)

    def test_check_932_ShouldReturnErrorOnInvalidCharacters(self):
        # As above, except since it is not written as a raw string, a normal check would identify it as 54 characters instead of 59. Regardless, it is invalid.
        parm = {
            'op': 'check',
            'cube': r'\.\.\.\.\\.\.\.\.\\.\.\.\.\\.\.\.\.\\.\.\.\.\\.\.\.\..\..\.'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube declaration - the cube contains invalid characters', status)

    def test_check_940_ShouldReturnErrorOnInvalidArrangementOfCenterPieces(self):
        parm = {
            'op': 'check',
            'cube': '123456234561345612456123561234612345654321615243314256'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain six unique center pieces', status)

    def test_check_941_ShouldReturnErrorOnInvalidArrangementOfCenterPieces(self):
        parm = {
            'op': 'check',
            'cube': 'OBRRBBBGWGBRWWRRGOYGWYGWGYBRGWOYBOROBOBYBYGOYWWGWORYOY'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain six unique center pieces', status)

    def test_check_950_ShouldReturnErrorOnInvalidArrangementOfCornerPieces(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbgrrrrrrrrrggggggggoooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of corner pieces', status)

    def test_check_951_ShouldReturnErrorOnInvalidArrangementOfCornerPieces(self):
        parm = {
            'op': 'check',
            'cube': '666666666122222222555555555444444244333333333411111111'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of corner pieces', status)

    def test_check_952_ShouldReturnErrorOnInvalidArrangementOfCornerPieces(self):
        parm = {
            'op': 'check',
            'cube': 'rooywowoybgwbbowbyoryyywowybbwrgrgygrbgworywyrgogryrgg'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of corner pieces', status)

    def test_check_960_ShouldReturnErrorOnInvalidArrangementOfEdgePieces(self):
        parm = {
            'op': 'check',
            'cube': 'rooywowobbgwrbowbyoryyywowybbwrgrgygrbgwobbwyrgogryrgg'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of edge pieces', status)

    def test_check_961_ShouldReturnErrorOnInvalidArrangementOfEdgePieces(self):
        parm = {
            'op': 'check',
            'cube': 'rooROoOobbBOrboObRorRRROoORbbOrBrBRBrbBOobbORrBoBrRrBB'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of edge pieces', status)

    def test_check_962_ShouldReturnErrorOnInvalidArrangementOfEdgePieces(self):
        parm = {
            'op': 'check',
            'cube': '544204041130514012452220402110535323513041102534352533'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of edge pieces', status)

    def test_check_963_ShouldReturnErrorOnInvalidArrangementOfEdgePieces(self):
        parm = {
            'op': 'check',
            'cube': 'OBRRBBBGWGORWWRRGOYGWYGWGYBRGWOYOOROBOBYRYGOYWWGWORYOY'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('error: invalid cube configuration - the cube does not contain a valid arrangement of edge pieces', status)

    def test_check_990_ShouldReturnErrorIfFaceColorDoesNotOccurNineTimes(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrggggggggooooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertTrue("face value does not occur 9 times" in status)
