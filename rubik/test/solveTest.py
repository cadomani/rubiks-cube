from unittest import TestCase
import rubik.solve as solve


class SolveTest(TestCase):
    def test_solve_010_ShouldReturnOkOnValidRotation(self):
        parm = {
            'op': 'solve',
            'cube': 'bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww',
            'rotate': 'F'
        }
        result = solve._solve(parm)
        self.assertIn('status', result)
        status = result.get('status', None)
        self.assertEqual('ok', status)
