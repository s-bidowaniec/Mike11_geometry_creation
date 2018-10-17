import unittest
from functions import *
from classes import *

class TestSomeFunctions(unittest.TestCase):

    def test_between(self):
        self.assertEqual(is_between(0, 0, 0, 2, 0, 4), True)
        self.assertEqual(is_between(0, 0, 2, 2, 4, 4), True)

    def test_distance(self):
        self.assertEqual(distance(0, 0, 0, 5), 5)
        self.assertEqual(distance(0, 5, 0, 5), 7.0710678118654755)

<<<<<<< HEAD
"""
class TestXs_tMethods(unittest.TestCase):
    def test_init_Xs_t(self):
        with open(r'Test\6.txt', 'r') as f:
            xs = XS_t(f)
        f.close()
        self.assertEqual(xs.name, '6')
        self.assertEqual(xs.rzeka, 'Dobka')
        self.assertEqual(xs.data, '2018-04-12')
        self.assertEqual(xs.type, 'most')
        self.assertEqual(len(xs.point_data), 18)

    def test_init_point(self):
        pkt = point(lp='1', x='10', y='10', z='5', odlRed='5', kod="kot", cos="zww", znacznik='10.0')
        self.assertEqual(pkt.lp, 1)
        self.assertEqual(pkt.x, 10)
        self.assertEqual(pkt.y, 10)
        self.assertEqual(pkt.z, 5)
        self.assertEqual(pkt.kod, 'kot')
        self.assertEqual(pkt.cos, ['zww'])

    def test_get_avarage_manning(self):
        with open(r'Test\6.txt', 'r') as f:
            xs = XS_t(f)
        f.close()
        #self.assertEqual(xs.get_avarage_manning(), None)
        #self.assertAlmostEqual(xs.avManning, 0.028845008380823725)
"""
class Test_line_intersection(unittest.TestCase):
    def test_line_intersectio(self):
        self.assertEqual(line_intersection(x1=0, y1=0, x2=50, y2=50, x3=0, y3=50, x4=50, y4=0), (25, 25, True, True))

class TestLinearEquation(unittest.TestCase):
    def test_linear_equation(self):
        array = [[0.928347365933718, 391.32], [3.20855993299333, 392.83], [5.5629339357402, 391.33]]
        self.assertEqual(linear_equation(array)(2.5), 392.6729846861197)
=======

class SimpleTest(unittest.TestCase):

    def test_value(self):
        self.assertEqual(2+2, 4)
        
>>>>>>> 40337fb3adfe80936708ee4e4078db4e3f5687c5
if __name__ == '__main__':
    unittest.main()
