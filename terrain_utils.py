import types
import terrain_modifiers
import numpy as np

import terrainblocks
from game import *
import random


def get_modifiers():
    """
    Obtains a reference to all the modifier functions.

    :return:
    """
    return [terrain_modifiers.__dict__.get(a) for a in dir(terrain_modifiers) if isinstance(getattr(terrain_modifiers, a, None), types.FunctionType)]


def destroy_circle(terrain, radius, origin):
    """
    Sets terrain within a certain radius of a point to 0.

    :param terrain: 2D numpy array of the entire terrain.
    :param radius: Int.
    :param origin: Tuple of (x, y)
    :return: None, as it *should* modify the terrain in place via side effects
    """
    subset = terrain[(origin[0] - radius) : (origin[0] + radius), (origin[1] - radius) : (origin[1] + radius)]

    # Create a distance array to every cell
    distances = np.zeros(shape=subset.shape)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            distances[i, j] = np.sqrt((i-radius)**2 + (j-radius)**2)

    subset[distances <= radius] |= -128


def get_planet_params(archetype, planet_info):
    """
    Retrieves a dictionary containing planetry information.
    
    :param archetype: A string.
    :param info: Various planetary factors.
    :return: 
    """
    # Load defaults and gradually overwrite
    params = default_values

    # DEBUGGING ONLY
    if planet_info is not None:
        params['gravity_mean'] = planet_info['size']
        params['modifier_params']['crater']['frequency'] = 0.01 + min(0.1, 0.5 / (0.1 + planet_info['dist_to_asteroid_belt'] ))
        planet_seed = planet_info['seed']
    else:
        planet_seed = 17

    r = random.Random(planet_seed)
    seed = r.getrandbits(32)
    r_params  = random.Random(seed)

    tparams = terrain_params[archetype]
    gravity = max(0.1, r_params.gauss(params['gravity_mean'], params['gravity_sd']))
    atmosphere = r_params.uniform( *tparams['atmos'] )
    params['modifier_params']['vegetation']['seed_mod'] = 1.0 - abs(atmosphere - 0.5)
    params['modifier_params']['crater']['radius_mean'] = max(6.0, 2.0 / max(0.2, atmosphere))
    params['modifier_params']['tunnel']['width_mean'] = 2.0 * tparams['softness']
    params['modifier_params']['tunnel']['width_sd']   = 0.1 * tparams['softness']
    params['gravity'] = gravity
    params['atmosphere'] = atmosphere

    # TODO Temp

    # TODO Oxygen

    # TODO Water

    return params


default_values = {
    'gravity_mean': 10,
    'gravity_sd': 0.3,
    'modifier_params':
        {'tunnel': {
            'frequency': 0.05,
            'depth_mean': 0.3,
            'depth_sd': 0.05,
            'width_mean': 2,
            'width_sd': 0.1
        },
        'crater': {
            'frequency': 0.02,
            'radius_mean': 10,
            'radius_sd': 2,
        },
        'vegetation': {
            'seed_mod': 1.0,
            'types':  [
                {   # Blue fungus
                    'grow_block':4,
                    'seedrate':0.8, #TODO: Scale with environment
                    'root_block':14,
                    'root_depth':1,
                    'grow_height':1,
                },
                {   # Purple leaves
                    'grow_block':3,
                    'seedrate':0.1, #TODO: Scale with environment
                    'root_block':4,
                    'root_depth':2,
                    'grow_height':5,
                },
                {   # Grass
                    'grow_block':9,
                    'seedrate':0.9, #TODO: Scale with environment
                    'root_block':2,
                    'root_depth':1,
                    'grow_height':1,
                },
            ]
        },
        'water': {
            # ...
        }
    }
}



# Ground "ground level"
# Layers are "dig depth"
terrain_params = {
    # Type: [ [ depth, ratio, blocktype ] ... ]
    'earth': {
        'atmos': (0.3, 0.5),
        'softness': 1.5,
        'depth': 80,
        'ratio': 0.5,
        'base': 1,          # Rock
        'layers': [
            [ 10, 0.6, 2 ],  # Dirt
        ]
    },
    'rock': {
        'atmos': (0.1, 0.5),
        'softness': 0.7,
        'depth': 80,
        'ratio': 0.7,
        'base': 1,          # Rock
        'layers': [
            [ 5, 0.3, 8 ],  # Dust
            [ 16, 0.6, 7 ],  # Cobble
        ]
    },
    'desert': {
        'atmos': (0.3, 0.9),
        'softness': 2.5,
        'depth': 80,
        'ratio': 0.2,
        'base': 10,          # Mars
        'layers': [
            [ 10, 0.2, 12 ], # Sand
            [ 16, 0.4, 11 ], # Red Sand
        ]
    },
    'other': {
        'atmos': (0.5, 0.9),
        'softness': 1.8,
        'depth': 80,
        'ratio': 0.7,
        'base': 13,          # Orange Rock
        'layers': [
            [ 10, 0.9, 14 ],  # Pink Sponge
        ]
    },
    'ice': {
        'atmos': (0.1, 0.5),
        'softness': 1.2,
        'depth': 80,
        'ratio': 0.5,
        'base': 1,           # Rock
        'layers': [
            [ 15, 0.3, 16 ], # Snow
            [ 10, 0.2, 5  ], # Ice
            [ 16, 0.8, 15 ], # Permafrost
        ]
    },
    'gas': {
        'atmos': (0.8, 1.0),
        'softness': 0.6,
        'depth': 500,
        'ratio': 0.3,
        'base': 17,          # Crystal
        'layers': [
            [ 10,  0.6, -128|20 ], # Cloud (WALL)
            [ 80,  0.5, -128|19 ], # Fog (WALL)
            [ 10,  0.2, 18  ],     # Crystal
        ]
    },
}
