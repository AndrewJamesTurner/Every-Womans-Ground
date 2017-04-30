import types
import terrain_modifiers
import numpy as np


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

    subset[distances <= radius] = 0

default_values = {
    'gravity_mean': -10,
    'gravity_sd': 0.05,
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
            'types':  [
                {
                    'seedrate':0.8,
                    'root_block':5,
                    'root_depth':1,
                    'grow_block':4,
                    'grow_height':1
                },
                {
                    'seedrate':0.1,
                    'root_block':4,
                    'root_depth':2,
                    'grow_block':3,
                    'grow_height':5
                }
            ]
        },
        'water': {
            # ...
        }
    }
}
