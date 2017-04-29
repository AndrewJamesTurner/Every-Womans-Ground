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
