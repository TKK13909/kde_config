 
import struct, random
from utils import util
import math

def draw_line(draw, x, y, length, angle, color, width):
    p1 = (0, -length)
    p2 = (0, length)

    p1r = ( p1[0]*math.cos(math.radians(angle)) - p1[1]*math.sin(math.radians(angle)),
            p1[1]*math.cos(math.radians(angle)) - p1[0]*math.sin(math.radians(angle)) )
    p2r = ( p2[0]*math.cos(math.radians(angle)) - p2[1]*math.sin(math.radians(angle)),
            p2[1]*math.cos(math.radians(angle)) - p2[0]*math.sin(math.radians(angle)) )

    p1r = util.sum_tuples(p1r, (x, y))
    p2r = util.sum_tuples(p2r, (x, y))
            
    draw.line((p1r, p2r), fill=color, width=width)

    