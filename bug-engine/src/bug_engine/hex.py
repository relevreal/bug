from collections import namedtuple


Point = namedtuple('Point', 'x y')


class Hex:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
    
    
    def __add__(self, other):
        pass
    
    
    def __sub__(self, other):
        pass

    
    def __mul__(self, other):
        try:
            hex = Hex(other * self.q, other * self.r, other * self.s)
        except:
            return NotImplemented
        else:
            return hex

    
HEX_DIRECTIONS = (
    Hex(1, 0, -1),
    Hex(1, -1, 0),
    Hex(0, -1, 1),
    Hex(-1, 0, 1),
    Hex(-1, 1, 0),
    Hex(0, 1, -1),
)