from rtree.types import Properties
from rtree.types import Statistics

class RTree(object):
    """ 
    """

    def __init__(self, properties = Properties()):
        self.stats = Statistics()
        self.max_capacity = properties['max_capacity']
        self.min_capacity = properties['min_capacity']
        self.k_means_size = properties['k_means_size']

    def search_range(self):
        """
        """
        pass

    def contains_point(self):
        """
        """
        pass

    def search_point(self):
        """
        """
        pass

    def insert(self):
        """
        """
        pass

    def delete(self):
        """
        """
        pass

    def search_k_nearest(self, k):
        """
        """
        pass

    def count(self):
        """
        """
        pass

    def intersection(self):
        """
        """
        pass

    def walk(self):
        """
        """
        pass

    def is_leaf(self):
        """
        """
        pass

    def choose_leaf(self):
        """
        """
        pass

    def adjust_tree(self):
        """
        """
        pass

    def handle_overflow(self):
        """
        """
        pass

    def find_leaf(self):
        """
        """
        pass

    def condense_tree(self):
        """
        """
        pass

    def split_node(self):
        """
        """
        pass
