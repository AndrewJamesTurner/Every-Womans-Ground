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
import terrain_utils


def tunnel_modifier(terrain, params, seed):
    """
    Creates tunnels in the terrain, one brick wide.

    :param terrain: A 2D numpy array of ints, detailing terrain types at each location.
    :param params: Dict, Values that are used in this modifier are:
        - num_tunnels
        - tunnel_depth
    :return: The modified terran as a 2D numpy array of ints.
    """
    width, height = terrain.shape
    r = random.Random(seed)
    digging_directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]  # Possible (x,y) pairs where can dig next square

    # Find how many tunnels will have and their x values
    num_tunnels = round(params['frequency'] * width)
    tunnel_x_points = [r.randint(0, width) for _ in range(num_tunnels)]

    # Identify coordinates for starting hole, uniformally distributed across terrain
    for x in tunnel_x_points:
        # Get ground height at this point
        col_depth = np.argmin(terrain[x, ]) - 1
        curr_y = col_depth
        curr_x = x

        # Generate tunnel depth
        tunnel_depth = int(r.gauss(params['depth_mean'], params['depth_sd']) * col_depth)

        for _ in range(tunnel_depth):
            # Choose direction that will dig in
            next_x, next_y = r.choice(digging_directions)

            # Dig a randomly generated width
            tunnel_radius = int(r.gauss(params['width_mean'], params['width_sd']))
            terrain_utils.destroy_circle(terrain, tunnel_radius, (curr_x, curr_y))

            # Update digging direction
            curr_x = curr_x + next_x if (curr_x + next_x < width) and (curr_x + next_x > 0) else curr_x
            curr_y = curr_y + next_y if (curr_y + next_y > 0) else curr_y

    return terrain


def crater_modifier(terrain, params, seed):
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
    r = random.Random(seed)

    # Find how many tunnels will have and their x values
    num_craters = round(params['frequency'] * width)
    crater_foci_x = [r.randint(0, width) for _ in range(num_craters)]

    # Identify coordinates for starting hole, uniformally distributed across terrain
    for x in crater_foci_x:
        # Get ground height at this point
        curr_y = np.argmin(terrain[x, ]) - 1

        # Generate a random radius
        crater_radius = int(r.gauss(params['radius_mean'], params['radius_sd']))

        if crater_radius == 0:
            continue

        # Obtain pixels that are covered by this radius
        terrain_utils.destroy_circle(terrain, crater_radius, (x, curr_y))

    return terrain


def vegetation_modifier(terrain, params, seed):
    width, height = terrain.shape

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


def water_modifier(terrain, params, seed):
    width, height = terrain.shape
    r = random.Random(seed)
    return terrain

