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
        self.assertEqual(status, 'ok')

    def test_check_020_ShouldReturnOkOnAlphanumericInput(self):
        parm = {
            'op': 'check',
            'cube': '999999999777777777111111111rrrrrrrrrgggggggggmmmmmmmmm'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'ok')

    def test_check_030_ShouldReturnOkOnMixedCaseAlphanumeric(self):
        parm = {
            'op': 'check',
            'cube': '999999999777777777888888888RRRRRRRRRooooooooonnnnnnnnn'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'ok')

    def test_check_040_ShouldReturnOkOnMixedCaseAlphabeticalWithSameLetters(self):
        parm = {
            'op': 'check',
            'cube': 'lllllllllLLLLLLLLLoooooooooOOOOOOOOOPPPPPPPPPppppppppp'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'ok')

    def test_check_050_ShouldReturnOkOnNumerical(self):
        parm = {
            'op': 'check',
            'cube': '999999999777777777111111111888888888666666666444444444'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'ok')

    def test_check_060_ShouldReturnOkOnValidArrangementOfCornerPieces(self):
        # This test is set to match a similar arrangement to EC, but it is perfectly solvable
        # due to the relevant face pieces not being contiguous yet
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggooooooooowyyyyyyyyywwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'ok')

    def test_check_910_ShouldReturnErrorOnMissingCube(self):
        parm = {
            'op': 'check'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the cube parameter is missing')

    def test_check_920_ShouldReturnErrorOnInvalidCubeType(self):
        parm = {
            'op': 'check',
            'cube': 999999999777777777111111111888888888666666666444444444
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the cube value is not a string')

    def test_check_930_ShouldReturnErrorOnNullCubeType(self):
        parm = {
            'op': 'check',
            'cube': None
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the cube value is not a string')

    def test_check_940_ShouldReturnErrorOnCubeOverLength(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the cube is not 54 characters in length')

    def test_check_950_ShouldReturnErrorOnCubeUnderLength(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrggggggggoooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the cube is not 54 characters in length')

    def test_check_960_ShouldReturnErrorIfFaceColorDoesNotOccurNineTimes(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbrrrrrrrrrggggggggooooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the "g" face does not occur 9 times')

    def test_check_970_ShouldReturnErrorOnInvalidArrangementOfCenterPieces(self):
        parm = {
            'op': 'check',
            'cube': '123456234561345612456123561234612345654321615243314256'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: invalid arrangement of center pieces')

    def test_check_980_ShouldReturnErrorOnInvalidArrangementOfCornerPieces(self):
        parm = {
            'op': 'check',
            'cube': 'bbbbbbbbbgrrrrrrrrrggggggggoooooooooyyyyyyyyywwwwwwwww'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: invalid cube arrangement')

    def test_check_981_ShouldReturnErrorOnInvalidArrangementOfCornerPieces(self):
        parm = {
            'op': 'check',
            'cube': '666666666122222222555555555444444244333333333411111111'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: invalid cube arrangement')

    def test_check_990_ShouldReturnErrorOnInvalidCharacters(self):
        parm = {
            'op': 'check',
            'cube': '%%%%%%%%%777777777.........RRRRRRRRR[[[[[[[[[MMMMMMMMM'
        }
        result = check._check(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual(status, 'error: the cube contains invalid characters')
