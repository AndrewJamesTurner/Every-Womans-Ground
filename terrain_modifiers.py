"""
    terrain_modifiers
    ~~~~~~~~~~~~~~~~~

    Contains functions for modifying terrain blocks.

    These are functions that are parameterised as follows:

    Args:
        terrain: A 2D numpy array of ints, detailing terrain types at each location.
        params: A dictionary containing appropriate parameters for each modifier.

    Returns:
        The modified terrain in the same format as the argument.
"""
import random
import numpy as np

import constants


def tunnel_modifier(terrain, params):
    """
    Creates tunnels in the terrain, one brick wide.

    :param terrain: A 2D numpy array of ints, detailing terrain types at each location.
    :param params: Dict, Values that are used in this modifier are:
        - num_tunnels
        - tunnel_depth
    :return: The modified terran as a 2D numpy array of ints.
    """
    digging_directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]  # Possible (x,y) pairs where can dig next square
    width, height = terrain.shape

    # Find how many tunnels will have and their x values
    num_tunnels = round(params['num'] * width)
    tunnel_x_points = np.random.randint(0, width, num_tunnels)

    # Identify coordinates for starting hole, uniformally distributed across terrain
    for x in tunnel_x_points:
        # Get ground height at this point
        col_depth = np.argmin(terrain[x, ]) - 1
        curr_y = col_depth
        curr_x = x

        # Generate tunnel depth
        tunnel_depth = int(np.random.normal(params['depth'], scale=constants.TERRAIN_TUNNEL_SD) * col_depth)

        for _ in range(tunnel_depth):
            # Set ground to 0
            terrain[curr_x, curr_y] = 0
            # Obtain next move
            next_x, next_y = random.choice(digging_directions)

            # Guard against digging off screen
            curr_x = curr_x + next_x if (curr_x + next_x < width) and (curr_x + next_x > 0) else curr_x
            curr_y = curr_y + next_y if (curr_y + next_y > 0) else curr_y

    return terrain


def crater_modifier(terrain, params):
    """
    Adds craters to the terrain.

    :param terrain: A 2D numpy array of ints, detailing terrain types at each location.
    :param params: Dict, Values that are used in this modifier are:
        - num_craters: Fraction of landscape that should have craters
        - crater_radius_mean: Average radius of craters as a ratio of screen size
        - crater_radius_sd: Standard deviation of cradius radius for this planet
    :return: The modified terran as a 2D numpy array of ints.
"""
    width, height = terrain.shape

    # Find how many tunnels will have and their x values
    num_craters = round(params['num'] * width)
    crater_foci_x = np.random.randint(0, width, num_craters)

    # Identify coordinates for starting hole, uniformally distributed across terrain
    for x in crater_foci_x:
        # Get ground height at this point
        curr_y = np.argmin(terrain[x, ]) - 1

        # Generate a random radius
        crater_radius = int(np.random.normal(params['radius_mean'], scale=params['radius_sd']))

        if crater_radius == 0:
            continue

        # Obtain pixels that are covered by this radius
        subset = terrain[(x - crater_radius) : (x + crater_radius), (curr_y - crater_radius) : (curr_y + crater_radius)]

        # Create a distance array to every cell
        distances = np.zeros(shape=subset.shape)
        for i in range(distances.shape[0]):
            for j in range(distances.shape[1]):
                distances[i, j] = np.sqrt((i-crater_radius)**2 + (j-crater_radius)**2)

        subset[distances <= crater_radius] = 0

    return terrain


def vegetation_modifier(terrain, params):
    width, height = terrain.shape

    seed = params['seed']
    r = random.Random(seed)
    for p in params['types']:
        rr = random.Random(r.getrandbits(32))
        seedrate   = p['seedrate']
        root_block = p['root_block']
        root_depth = p['root_depth']
        grow_block = p['grow_block']
        grow_height= p['grow_height']
        for x in range(0,width):
            # Do we seed or not?
            if not rr.random() < seedrate: continue

            # Search the column
            roots_needed = round(root_depth * rr.normalvariate(1, 0.3))
            grow_count   = round(grow_height * rr.normalvariate(1, 0.3))
            roots_found = 0
            for y in reversed(range(0, height)):
                b = terrain[x,y]
                if b == 0:
                    continue
                if b != root_block:
                    break
                roots_found += 1
                if roots_found >= roots_needed:
                    # Success - seed the plant!
                    for yy in range(y + roots_needed, min(height, y + roots_needed + grow_count)):
                        terrain[x,yy] = grow_block
                    break
    return terrain


def water_modifier(terrain, params):
    return terrain

