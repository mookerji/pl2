import math

# TODO: This produces a weird circular dependency
# from rtree.utils import hilbert_encode


class Rectangle(object):
    """ A rectangle, axis-aligned with a Euclidean basis. 
    The origin is at the lower-left.
    """

    __slots__ = {'left', 'right', 'bottom', 'top'}

    __hilbert_res = 32

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
            merged = merged.get_mbr(rect)
        return merged

    @property
    def hilbert_value(self):
        """ Returns the Hilbert value of the rectangle centroid.
        """
        x, y = self.centroid
        return hilbert_encode((int(x), int(y)), Rectangle.__hilbert_res)

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
    
    def get_mbr(self, rect):
        """ Returns the minimum bounding rectangle with another rectangle.
        """
        left = min(self.left, rect.left)
        right = max(self.right, rect.right)
        bottom = min(self.bottom, rect.bottom)
        top = max(self.top, rect.top)
        return Rectangle((left, bottom), (right, top))

    def get_mbr_point(self, point):
        """ Returns the minimum bounding rectangle with a point
        """
        rect = Rectangle(point, point)
        return self.get_mbr(rect)
    
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


def hilbert_encode((x, y), r):
    """Gives a Hilbert fractal encoding of a grid point (x, y) in a grid of
    resolution r (yielding a square grid of length 2**r).
    """
    mask = (1 << r) - 1
    hodd = 0
    heven = x ^ y
    notx = ~x & mask
    noty = ~y & mask
    temp = notx ^ y
    v0 = 0
    v1 = 0
    for k in xrange(1, r):
        v1 = ((v1 & heven) | ((v0 ^ noty) & temp)) >> 1
        v0 = ((v0 & (v1 ^ notx)) | (~v0 & (v1 ^ noty))) >> 1
    hodd = (~v0 & (v1 ^ x)) | (v0 & (v1 ^ noty))
    return interleave_bits(hodd, heven)


def interleave_bits(odd, even):
    """ Returns bit string from interleaving odd and even bit strings.
    """
    val = 0
    max0 = max(odd, even)
    n = 0
    while (max0 > 0):
        n += 1
        max0 >>= 1
    for i in xrange(n):
        bitMask = 1 << i
        a = (1 << (2*i)) if (even & bitMask) > 0  else 0
        b = (1 << (2*i+1)) if (odd & bitMask) > 0 else 0
        val += a + b
    return val
