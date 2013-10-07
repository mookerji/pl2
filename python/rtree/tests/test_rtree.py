import unittest

from rtree.types import LeafEntry
from rtree.types import PointerEntry
from rtree.types import Rectangle


class RTreeTests(unittest.TestCase):
    def test_pointer_entry(self):
        self.assertTrue(False)

    def test_leaf_entry(self):
        self.assertTrue(False)

    def test_leaf_creation(self):
        self.assertTrue(False)
        
    def test_properties(self):
        self.assertTrue(False)

    def test_hilbert_access(self):
        self.assertTrue(False)

    def test_iter(self):
        self.assertTrue(False)

    def test_search_range(self):
        self.assertTrue(False)
        
    def test_adjust_tree(self):
        self.assertTrue(False)
        
    def test_get_parent_entry(self):
        self.assertTrue(False)
        
    def test_handle_overflow(self):
        self.assertTrue(False)

    def test_handle_shift(self):
        self.assertTrue(False)

    def test_handle_split(self):
        self.assertTrue(False)

    def test_find_leaf(self):
        self.assertTrue(False)

    def test_insert(self):
        self.assertTrue(False)
        
    def test_delete(self):
        self.assertTrue(False)
    
    def test_search_knn(self):
        self.assertTrue(False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RectangleTest)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    unittest.main()
