import unittest
from functions import *

class TestStringMethods(unittest.TestCase):

    def test_between(self):
        self.assertEqual(is_between(0, 0, 0, 2, 0, 4), True)
        self.assertEqual(is_between(0, 0, 2, 2, 4, 4), True)

    def test_distance(self):
        self.assertEqual(distance(0, 0, 0, 5), 5)
        self.assertEqual(distance(0, 5, 0, 5), 7.0710678118654755)
if __name__ == '__main__':
    unittest.main()