import unittest

from rtree.types import Rectangle


class RectangleTests(unittest.TestCase):
    def test_creation(self):
        r = Rectangle((10, 10), (15, 15))
        self.assertTrue(r is not None)
        self.assertTrue(r != Rectangle.get_empty())
        s = Rectangle((10, 10), (15, 15))
        self.assertTrue(r == s)

    def test_properties(self):
        r = Rectangle((10, 10), (15, 15))
        self.assertTrue(r.left == 10)
        self.assertTrue(r.right == 15)
        self.assertTrue(r.bottom == 10)
        self.assertTrue(r.top == 15)
        self.assertTrue(r.height == 5)
        self.assertTrue(r.width == 5)
        self.assertTrue(r.area == 25)
        self.assertTrue(r.centroid == (12.5, 12.5))
        s = Rectangle((15, 15), (10, 10))
        self.assertTrue(r == s)

    def test_contain_point(self):
        r = Rectangle((10, 10), (15, 15))
        self.assertTrue(r.contains_point(r.centroid))

    def test_contain_rectangles(self):
        r = Rectangle((10, 10), (15, 15))
        x, y = r.centroid
        self.assertTrue(r.contains_rect(Rectangle(r.centroid, (x+1, y+1))))
        self.assertFalse(r.contains_rect(Rectangle(r.centroid, (x+10, y+10))))

    def test_intersection(self):
        r = Rectangle((10, 10), (15, 15))
        x, y = r.centroid
        self.assertTrue(r.intersects_rect(Rectangle(r.centroid, (x+1, y+1))))
        self.assertTrue(r.intersects_rect(Rectangle(r.centroid, (x+10, y+10))))

        r = Rectangle((0, 0), (10, 10))
        s = Rectangle((10, 10), (15, 15))
        self.assertFalse(r.intersects_rect(s))

        r = Rectangle((0, 0), (10, 10))
        s = Rectangle((12, 12), (15, 15))
        self.assertFalse(r.intersects_rect(s))

    def test_mbr(self):
        r = Rectangle((0, 0), (10, 10))
        s = Rectangle((10, 10), (15, 15))
        t = Rectangle((0, 0), (15, 15))
        self.assertTrue(r.get_mbr(s) == t)


class PageTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RectangleTests)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(PageTests)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    unittest.main()
