import unittest
import classes
import pickle

class TestClasses(unittest.TestCase):

    def test_distance(self):
        self.assertEqual(classes.distance(0,0,0,10), 10)
        self.assertEqual(classes.distance(0, 0, 5, 0), 5)
    def test_is_between(self):
        self.assertTrue(classes.is_between(0,0,2,2,4,4))
        self.assertTrue(classes.is_between(0,0,2,0,4,0))
    def test_is_between2(self):
        self.assertTrue(classes.is_between(0,0,2,2,4,4))
        self.assertTrue(classes.is_between(0,0,2,0,4,0))
        #self.assertTrue(classes.is_between(0, 1, 0, 2, 0, 4))

    #xsT = pickle.load(open("XS_t.p", "rb"))
    def test_get_culver_len(self):
        xsT = pickle.load(open("XS_t.p", "rb"))
        xsT.get_culver_len()
        #print(xsT.culvert_downS)
        self.assertEqual(round(xsT.culvert_len, 2), 6.21)