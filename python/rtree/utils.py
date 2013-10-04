# Useful utilities.
# See http://stackoverflow.com/questions/106237/calculate-the-hilbert-value-of-a-point-for-use-in-a-hilbert-r-tree

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
