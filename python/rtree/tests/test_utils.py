import unittest

from rtree.utils import hilbert_encode


class HilbertCurveTests(unittest.TestCase):
    def test_hilbert_n1(self):
        self.assertTrue(hilbert_encode((0, 0), 1) is 0)
        self.assertTrue(hilbert_encode((0, 1), 1) is 1)
        self.assertTrue(hilbert_encode((1, 1), 1) is 2)
        self.assertTrue(hilbert_encode((1, 0), 1) is 3)

    def test_hilbert_n2(self):
        self.assertTrue(hilbert_encode((0, 0), 2) is 0)
        self.assertTrue(hilbert_encode((0, 1), 2) is 3)
        self.assertTrue(hilbert_encode((1, 1), 2) is 2)
        self.assertTrue(hilbert_encode((1, 0), 2) is 1)
        self.assertTrue(hilbert_encode((0, 2), 2) is 4)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HilbertCurveTests)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    unittest.main()
