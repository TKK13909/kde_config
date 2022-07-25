 
import struct, random
from utils import util

def _rint():
    return random.randint(0, 255)

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return struct.unpack('BBB', bytes.fromhex(hex))

def rgb_to_hex(r):
    return ('#%02X%02X%02X' % (r[0], r[1], r[2]))

def random_hex():
    return ('#%02X%02X%02X' % (_rint(),_rint(),_rint()))

def random_rgb():
    return (_rint(), _rint(), _rint(), 255)

def col_lerp(c1, c2, ratio):
    r1, g1, b1 = c1
    r2, g2, b2 = c2

    dr = r2-r1
    dg = g2-g1
    db = b2-b1

    return (int(r1+dr*ratio), int(g1+dg*ratio), int(b1+db*ratio))

# from https://stackoverflow.com/questions/40233986/python-is-there-a-function-or-formula-to-find-the-complementary-colour-of-a-rgb
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(rgb):
    r, g, b = rgb
    k = hilo(r, g, b)
    c = tuple(k - u for u in (r, g, b))
    c = tuple(util.clamp(0, x, 255) for x in c)
    return c

def dim(rgb, percent):
    return tuple(int(x*percent) for x in rgb)

def random_close(color):
    total_distance = 15
    current_distance = 0
    color = list(color)
    while(current_distance <= total_distance):
        current = random.randint(4, 10) * random.choice([-1, 1])
        current = util.clamp(total_distance - current_distance, current, current_distance)

        index = random.randint(0, 2)

        tentative = color[index] + current
        if tentative < 0:
            tentative -= current
        elif tentative > 255:
            tentative += current
        color[index] = tentative

        current_distance += abs(current)

    return tuple(color)