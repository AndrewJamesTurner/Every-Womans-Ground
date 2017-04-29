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


def add_tunnels(terrain, params):
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
    num_tunnels = round(params['num_tunnels'] * width)
    tunnel_x_points = np.random.randint(0, width, num_tunnels)

    # Identify coordinates for starting hole, uniformally distributed across terrain
    for x in tunnel_x_points:
        # Get ground height at this point
        col_depth = np.argmin(terrain[x, ]) - 1
        curr_y = col_depth
        curr_x = x

        # Generate tunnel depth
        tunnel_depth = int(np.random.normal(params['tunnel_depth'], scale=constants.TERRAIN_TUNNEL_SD) * col_depth)

        for _ in range(tunnel_depth):
            # Set ground to 0
            terrain[curr_x, curr_y] = 0
            # Obtain next move
            next_x, next_y = random.choice(digging_directions)

            # Guard against digging off screen
            curr_x = curr_x + next_x if (curr_x + next_x < width) and (curr_x + next_x > 0) else curr_x
            curr_y = curr_y + next_y if (curr_y + next_y > 0) else curr_y

    return terrain

def add_craters(terrain, params):
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
    num_craters = round(params['num_craters'] * width)
    crater_foci_x = np.random.randint(0, width, num_craters)

    # Identify coordinates for starting hole, uniformally distributed across terrain
    for x in crater_foci_x:
        # Get ground height at this point
        curr_y = np.argmin(terrain[x, ]) - 1

        # Generate a random radius
        crater_radius = int(np.random.normal(params['crater_radius_mean'], scale=params['crater_radius_sd']))

        # Obtain pixels that

    return terrain


def add_vegetation(terrain, params):
    return terrain


def add_water(terrain, params):
    return terrain


def add_water(terrain, params):
    return terrain



