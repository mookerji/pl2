import math

class Statistics(dict):
    """ Keeps track of R-Tree operation statistics and functions calls.
    """
    def __init__(self, *args, **kwargs):
        super(Statistics, self).__init__(*args, **kwargs)        
        self['overflow'] = kwargs.get("overflow", 0)
        self['split'] = kwargs.get("split", 0)
        self['condense'] = kwargs.get("condense", 0)
        self['leaf_nodes'] = kwargs.get("leaf_nodes", 0)
        self['internal_nodes'] = kwargs.get("internal_nodes", 0)
        self['tree_height'] = kwargs.get("tree_height", 0)


class Properties(dict):
    """ Configures the RTree.
    """
    
    def __init__(self, *args, **kwargs):
        super(Properties, self).__init__(*args, **kwargs)
        self['max_capacity'] = kwargs.get("max_capacity", 0)
        self['min_capacity'] = kwargs.get("min_capacity", 0)
        self['k_means_size'] = kwargs.get("k_means_size", 0)


class Rectangle(object):
    """ A rectangle, axis-aligned with a Euclidean basis. 
    The origin is at the lower-left.
    """

    __slots__ = {'left', 'right', 'bottom', 'top'}

    def __init__(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        self.left = min(x1, x2)
        self.right = max(x1, x2)
        self.bottom = min(y1, y2)
        self.top = max(y1, y2)
    
    @classmethod 
    def get_empty(cls):
        return Rectangle((0, 0), (0, 0))

    @classmethod 
    def merge_by_mbr(cls, rects):
        merged = Rectangle.get_empty()
        for rect in rects:
            merged = merged.get_minimum_bounding_rect(rect)
        return merged

    @property
    def hilbert_value(self):
        """ Returns the Hilbert value of the rectangle centroid.
        """
        assert False

    @property 
    def centroid(self):
        h = self.left + self.width/2.
        v = self.bottom + self.height/2.
        return (h, v)
        
    @property 
    def area(self):
        return self.width*self.height
    
    @property
    def width(self):
        return self.right - self.left
        
    @property
    def height(self):
        return self.top - self.bottom
    
    @property
    def diagonal_length(self):
        return math.sqrt(self.width**2 + self.height**2)

    @property
    def coordinates(self):
        """ Clockwise order starting at lower-right: a->b->c->d.
        """
        a = (self.left, self.bottom)
        b = (self.left, self.top)
        c = (self.right, self.top)
        d = (self.right, self.bottom)
        return [a, b, c, d]

    def contains_point(self, point):
        x, y = point
        return (self.left <= x <= self.right) and (self.bottom <= y <= self.top)
        
    def contains_rect(self, rect):
        min_rect = (rect.left, rect.bottom)
        max_rect = (rect.right, rect.top)
        return self.contains_point(min_rect) and self.contains_point(max_rect)

    def get_intersect_area(self, rect):
        assert False

    def intersects_rect(self, rect):
        return self.right > rect.left and self.left < rect.right and self.top > rect.bottom and self.bottom < rect.top
    
    def get_minimum_bounding_rect(self, rect):
        """ Returns the minimum bounding rectangle with another rectangle.
        """
        left = min(self.left, rect.left)
        right = max(self.right, rect.right)
        bottom = min(self.bottom, rect.bottom)
        top = max(self.top, rect.top)
        return Rectangle((left, bottom), (right, top))

    def get_minimum_bounding_rect_point(self, point):
        """ Returns the minimum bounding rectangle with a point
        """
        rect = Rectangle(point, point)
        return self.get_minimum_bounding_rect(rect)
    
    def get_expanded(self, n):
        assert False
        
    def get_dotstring_repr(self):
        """ Returns a string for Graphviz representation
        """
        assert False

    def __eq__(self, rect):
        return (self.left == rect.left) and (self.right == rect.right) \
            and (self.top == rect.top) and (self.bottom == rect.bottom) \
        
    def __repr__(self):
        return "%s<%r>" % (self.__class__.__name__, self.coordinates)


class Page(object):
    """
    """

    def __init__(self):
        pass

    def __repr__(self):
        pass
