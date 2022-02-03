from unittest import TestCase
import rubik.solve as solve


class SolveTest(TestCase):
    def test_solve_010_ShouldReturnOkOnValidRotation(self):
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
        self.assertEqual('ok', status)
        
        cube = result.get('cube', None)
        self.assertEqual(expected['cube'], cube)
        
        
