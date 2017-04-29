import math
import random
import numpy
import shapes

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

def new_terrain_array(width, height):
    return numpy.zeros((width, height), int)

def rasterize_heightmap(terrain, heightmap, blocktype):
    length = len(heightmap)
    for x in range(0, length):
        for y in range(0,math.ceil(heightmap[x])):
            terrain[x,y] = blocktype

def generate_planet_test(seed, width, height):
    # Subseeding
    r = random.Random(seed)
    seed_rockbase = r.getrandbits(32)

    # Generators
    terrain = new_terrain_array(width, height)
    rock_heightmap = generate_fractal_heightmap(
        seed_rockbase, width, height / 2, 0.6)
    rasterize_heightmap(terrain, rock_heightmap, 1)

    return terrain

def print_terrain(terrain, chars):
    width, height = terrain.shape
    for y in reversed(range(0,height)):
        line = [ terrain[x, y] for x in range(0,width) ]
        list = [ chars[int(i)] for i in line ]
        print( ''.join(list) )

def create_terrain(coords, world):
    """
    Creates an array of TerrainBlock items, which ultimately subclass GameObject and
    can be drawn by pygame.

    :param biome: A string, available choices are:
        - 'desert'
        - 'forest'
        - 'lava'
        - 'water'
        - 'ice'
    :param coords: A list of (x, y) tuples.
    :param world: A reference to a world object (pygame object).
    :return: A list of TerrainBlock objects.
    """
    terrain = []
    width, height = coords.shape
    for w in range(width):
        for h in range(height):
            blocktype = coords[w, h]
            if blocktype > 0:
                terrain.append(shapes.terrain_block_factory(blocktype, (w - round(0.5*width), h - round(0.5*height)), world))
    return terrain
