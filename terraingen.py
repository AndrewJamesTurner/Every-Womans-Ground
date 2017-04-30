import math
import random
import numpy
import shapes

from game import *
import terrainblocks
import terrain_utils

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
            while y < heightmap[x]:
                terrain[x,y] = blocktype
                y += 1

def add_heightmaps(map1, map2):
    return [ sum(e) for e in zip(map1, map2) ]

def sub_heightmaps(map1, dig1):
    return [ a-b for (a,b) in zip (map1, dig1) ]

def generate_planet_terrain(seed, archetype, width):
    # Get generator parameters
    params = terrain_utils.terrain_params[archetype]

    # Subseeding
    r = random.Random(seed)
    seed_groundbase = r.getrandbits(32)
    dig_seeds = [ r.getrandbits(32) for l in params['layers'] ]

    # Generators
    maplayers = []
    heightmap = generate_fractal_heightmap(
        seed_groundbase, width, params['depth'], params['ratio'])
    max_height = math.ceil(max(heightmap))

    for i, l in enumerate( params['layers'] ):
        depth, ratio, blocktype = l
        digdepth = generate_fractal_heightmap(dig_seeds[i], width, depth, ratio)
        maplayers.append([ heightmap, blocktype ])
        heightmap = sub_heightmaps(heightmap, digdepth)
    maplayers.append([heightmap, params['base']])
    maplayers.reverse()
    maplayers[0][0] = [ max(1.5, h) for h in maplayers[0][0] ]

    terrain = new_terrain_array(width, max_height)
    rasterize_heightmap_layers(terrain, maplayers )
    return terrain

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
        seed_icebase, width, 3, 0.6)

    dirt_heightmap = sub_heightmaps(ground_heightmap, ice_depthmap)
    rock_heightmap = sub_heightmaps(dirt_heightmap, dirt_depthmap)

    rasterize_heightmap_layers(terrain, [
        [ rock_heightmap,   1 ],
        [ dirt_heightmap,   2 ],
        [ ground_heightmap, 5] ] )

    return terrain

def generate_terrain_test(width, height):
    # Generate a stripe test of the terrain
    terrain = new_terrain_array(width, height)
    layers = [ [[b] * width,b] for b in range(0,len(terrainblocks.BLOCK_DEFS)) ]
    rasterize_heightmap_layers(terrain, layers )

    return terrain

def get_initial_position(terrain, x, yoffset):
    width, height = terrain.shape
    c = x+int(width/2)
    for y in reversed(range(0,height)):
        if terrain[c, y] > 0:
            return (x,y+yoffset)

def print_terrain(terrain, chars):
    width, height = terrain.shape
    for y in reversed(range(0,height)):
        line = [ terrain[x, y] for x in range(0,width) ]
        list = [ chars[int(i)] for i in line ]
        print( ''.join(list) )
