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


class TestXs_tMethods(unittest.TestCase):
    def test_init_Xs_t(self):
        with open(r'Test\Xs_t_03.txt', 'r') as f:
            xs = XS_t(f)
        f.close()
        self.assertEqual(xs.name, '03')
        self.assertEqual(xs.rzeka, 'Niagara')
        self.assertEqual(xs.data, '24.02.1576')
        self.assertEqual(xs.type, 'most')
        self.assertEqual(len(xs.point_data), 37)

    def test_init_point(self):
        pkt = point(lp='1', x='10', y='10', z='5', kod="kot", cos="zww")
        self.assertEqual(pkt.lp, 1)
        self.assertEqual(pkt.x, 10)
        self.assertEqual(pkt.y, 10)
        self.assertEqual(pkt.z, 5)
        self.assertEqual(pkt.kod, 'kot')
        self.assertEqual(pkt.cos, ['zww'])

    def test_get_avarage_manning(self):
        with open(r'Test\Xs_t_03.txt', 'r') as f:
            xs = XS_t(f)
        f.close()
        self.assertEqual(xs.get_avarage_manning(), None)
        self.assertAlmostEqual(xs.avManning, 0.0270015375072781)


if __name__ == '__main__':
    unittest.main()