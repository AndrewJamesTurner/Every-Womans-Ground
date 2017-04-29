import math
import random

from game import *

def generate_fractal_heightmap(seed, length, max_height, ratio):
    elements = 2 ** math.ceil( math.log( length - 1, 2) ) + 1
    ary = [None] * elements
    error = max_height / 2
    r = random.Random(seed)
    step = elements - 1

    ary[0]          = r.uniform(0,max_height)
    ary[elements-1] = r.uniform(0,max_height)
    while step > 1:
        offset = step >> 1
        for i in range(offset, elements, step):
            print(i)
            assert( ary[i] is None )
            a = ary[i - offset]
            b = ary[i + offset]
            h = (a + b) / 2
            h += r.uniform(-error, error)
            h = max(0, min(h, max_height))
            ary[i] = h
        step >>= 1     # Halve the step size
        error *= ratio # Drop the error

    return ary[0:length]
