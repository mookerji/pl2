import unittest

from rtree.types import Rectangle


class RTreeTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RectangleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
