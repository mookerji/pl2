import bisect
import itertools


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


class PointerEntry(object):
    """ Inner node entry pointing to an inner region.
    """

    # TODO: UPDATE THESE SLOTS
    __slots__ = {'mbr', 'child', 'mhv'}

    def __init__(self, mbr, child):
        self.mbr = mbr 
        self.child = child
        self.mhv = None

    def get_dotstring_repr(self):
        assert False

    # def __repr__(self):
    #     ans = (self.__class__.__name__, self.m, self.child.mbr)
    #     return "%s<%r, %r>" % ans


class LeafEntry(object):
    """ Object stored at an entry.
    """

    __slots__ = {'mbr', 'obj_id', 'obj', 'mhv'}

    def __init__(self, mbr, obj_id, obj = None):
        self.mbr = mbr
        self.obj_id = obj_id
        self.obj = obj
        self.mhv = mbr.hilbert_value

    # def __repr__(self):
    #     ans = (self.__class__.__name__, self.mbr, self.obj_id, self.obj)
    #     return "%s<%r, %d, %r>" % ans


class RTreeNode(object):
    """ 
    A page is collection of entries. A page can either be for an inner node, in
    which case all of its entries are PointerEntries; or it can be a leaf node, and 
    all of its entries are LeafEntries. It has a fixed capacity.
    """

    # __slots__ = {'is_root', 'stats', 'max_capacity', 'min_capacity', 'k_means_size', 'page_entries', 'mbr'}

    def __init__(self, is_root = False, parent = None, props = Properties(), stats = Statistics(), page_entries = None):
        self.is_root = is_root
        self.stats = stats
        self.max_capacity = props['max_capacity']
        self.min_capacity = props['min_capacity']
        self.k_means_size = props['k_means_size']
        assert not page_entries or (len(page_entries) <= self.max_capacity)
        self.page_entries = page_entries if page_entries else []
        self.parent = parent 
        #self.mbr = Rectangle.merge_by_mbr([entry.mbr for entry in self.page_entries])

    @property 
    def is_leaf_node(self):
        return len(self.page_entries) > 0 and isinstance(self.page_entries[0], LeafEntry)

    @property
    def is_full_node(self):
        return len(self.page_entries) == self.max_capacity

    @property
    def mhv_values(self):
        return [entry.mhv for entry in self.page_entries]

    @property 
    def num_children(self):
        return 0 if self.is_leaf_node else len(self.page_entries)
        
    @property
    def mbr(self):
        return Rectangle.merge_by_mbr([entry.mbr for entry in self.page_entries])

    @property
    def mhv(self):
        return max([entry.mhv for entry in self.page_entries])

    @property 
    def num_cohort(self):
        return len(self.parent.page_entries)
        
    @property
    def cohort_entries(self):
        entries = [entry.child.page_entries for entry in self.parent.page_entries]
        return list(itertools.chain.from_iterable(entries))

    def iter(self, pred):
        """ Walks all the pages and page entries in a DFS fashion.
        TODO: Implement as an iterator and re-express search operations over the tree.
        """
        assert False

    def search_range(self, query_rectangle, objects = False):
        """Finds all rectangles that are stored in an R-tree , which
        are intersected by a query rectangle. 
        """
        if objects:
            assert False, "Returning full objects not implemented yet."
        ans = []
        for entry in self.page_entries:
            if entry.mbr.intersects_rect(query_rectangle) and self.is_leaf_node:
                ans.append(entry.obj_id)
            elif entry.mbr.intersects_rect(query_rectangle):
                ans.extend(entry.child.search_range(query_rectangle, objects))
        return ans

    def contains_point(self, point):
        """ 
        """
        assert False

    def search_point(self, point, objects = False):
        """Finds all rectangles that are stored in an RTree, which
        contain the query point. 
        """
        if objects:
            assert False, "Returning full objects not implemented yet."
        ans = []
        for entry in self.page_entries:
            if entry.mbr.contains_point(query_rectangle) and self.is_leaf_node:
                ans.append(entry.obj_id)
            elif entry.mbr.contains_point(query_rectangle):
                ans.extend(entry.child.search_point(query_rectangle, objects))
        return ans

    def insert(self, leaf_entry):
        """ Inserts a new entry leaf_entry in an RTree
        """
        leaf = self.choose_leaf(leaf_entry)
        if not leaf.is_full_node:
            index = self.next_entry_by_mhv(leaf_entry.mhv)
            self.page_entries.insert(index, leaf_entry)
        else:
            split_node = leaf.handle_overflow(leaf_entry)
        self.adjust_tree(split_node)

    def adjust_tree(self, split_node = None):
        """Propagate from node, adjusting covering rectangles and propagating nodes
        splits as necessary.
        """
        if self.is_root:
            return 
        parent = self.parent
        if not parent.is_full_node:
            index = parent.next_entry_by_mhv(split_node.mhv)
            parent.page_entries.insert(index, split_node)
        else:
            new_split = parent.handle_overflow(split_node)
        # adjust
        # recurse

    def get_parent_entry(self):
        for entry in self.parent.page_entries:
            if entry.child is self:
                return entry

    def handle_overflow(self, leaf_entry):
        """ Returns a new node if an split has actually occurred, or None.
        """
        n = self.num_cohort
        e = self.cohort_entries + leaf_entry
        e = sorted(e, key = lambda entry: entry.mhv, reverse = True)
        if len(e) <= n*self.max_capacity:
            return self._handle_shift(e)
        else:
            return self._handle_split(e)            

    def _handle_shift(self, sorted_entries):
        """ If we have space amongst the sibling nodes, redistribute the entries 
        in sorted order.
        """ 
        for i in xrange(self.parent.num_children):
            self.parent.page_entries[i].child.page_entries = []
            j = 0
            new_allocation = len(e)/self.parent.num_children
            while j < new_allocation and len(e) > 0:
                self.parent.page_entries[i].child.page_entries.append(e.pop())
                j += 1
        return None

    def _handle_split(self, sorted_entries):
        """ If we lack space amongst the sibling nodes, add a new node and 
        redistribute the entries in sorted order.
        """ 
        new_node = RTreeNode(is_root = False, parent = None)
        for i in xrange(self.parent.num_children):
            self.parent.page_entries[i].child.page_entries = []
            new_allocation = len(e)/(self.parent.num_children + 1)
            while j < new_allocation and len(e) > 0:
                self.parent.page_entries[i].child.page_entries.append(e.pop())
        return new_node
            

    def find_leaf(self, leaf_entry):
        """ Find the leaf containing the leaf_entry.
        """
        for entry in self.page_entries:
            if self.is_leaf_node and entry.mbr == leaf_entry.mbr:
                return entry
            elif not self.is_leaf_node and entry.mbr.intersects_rect(entry.mbr):
                return entry.child.find_each(leaf_entry)
        return None
            
    def choose_leaf(self, leaf_entry):
        """ Returns the leaf node in which to place the new leaf_entry.
        """
        if self.is_leaf_node:
            return self
        else:
            next_entry = self.next_entry_by_mhv(leaf_entry.mhv)
            child = self.page_entries[next_entry].child
            return child.choose_leaf(leaf_entry)

    def next_entry_by_mhv(self, h):
        """ Returns next page entry with the minimum Hilbert value greater than h.
        """ 
        return bisect.bisect_left(self.mhv_values, h)

    def delete(self, leaf_entry):
        """ Deletes the leaf_entry.
        """
        leaf = self.find_leaf(leaf_entry)
        if leaf is None:
            return 
        for i in xrange(len(leaf.entries)):
            entry = leaf.entries[i]
            if entry.mbr == leaf_entry.mbr:
                leaf.entries.pop(i)
        #         leaf.condense_tree()
        #         break
        # if self.num_children == 1:
        #     self = self.page_entries[0].child
        #     self.parent = None

    def search_k_nearest(self, k, point):
        """ Returns the k-nearest neighbors from a specified point
        """
        assert False

from itertools import izip
argmax = lambda array: max(izip(array, xrange(len(array))))[1]
