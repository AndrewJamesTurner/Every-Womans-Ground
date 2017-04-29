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

def rasterize_heightmap_layers(terrain, parameters):
    width = terrain.shape[0]
    for x in range(0, width):
        y = 0
        for p in parameters:
            heightmap,blocktype = p
            print("y=%d, h=%d, b=%d" % (y, heightmap[x], blocktype))
            while y < heightmap[x]:
                terrain[x,y] = blocktype
                y += 1

def add_heightmaps(map1, map2):
    return [ sum(e) for e in zip(map1, map2) ]

def sub_heightmaps(map1, dig1):
    return [ a-b for (a,b) in zip (map1, dig1) ]

def generate_planet_test(seed, width, height):
    # Subseeding
    r = random.Random(seed)
    seed_groundbase = r.getrandbits(32)
    seed_dirtbase = r.getrandbits(32)
    seed_icebase = r.getrandbits(32)

    # Generators
    terrain = new_terrain_array(width, height)
    ground_heightmap = generate_fractal_heightmap(
        seed_groundbase, width, height, 0.5)

    dirt_depthmap = generate_fractal_heightmap(
        seed_dirtbase, width, 6, 0.6)

    ice_depthmap = generate_fractal_heightmap(
        seed_icebase, width, 2, 0.6)

    dirt_heightmap = sub_heightmaps(ground_heightmap, ice_depthmap)
    rock_heightmap = sub_heightmaps(dirt_heightmap, dirt_depthmap)

    rasterize_heightmap_layers(terrain, [
        [ rock_heightmap,   1 ],
        [ dirt_heightmap,   4 ],
        [ ground_heightmap, 5] ] )

    return terrain

def print_terrain(terrain, chars):
    width, height = terrain.shape
    for y in reversed(range(0,height)):
        line = [ terrain[x, y] for x in range(0,width) ]
        list = [ chars[int(i)] for i in line ]
        print( ''.join(list) )
