
import os

import pygame

from constants import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

pygame.init()

CAMERA_POSITION = (0, 0)

def world_to_screen_coordinates(world_coords):
    window_coords = (   world_coords[0] - CAMERA_POSITION[0],
                        world_coords[1] - CAMERA_POSITION[1] )
    screen_coords = (   SCREEN_WIDTH  / 2 + window_coords[0] * PPM,
                        SCREEN_HEIGHT / 2 - window_coords[1] * PPM )
    return screen_coords

def screen_to_world_coordinates(screen_coords):
    window_coords = (   (SCREEN_WIDTH  / 2 + screen_coords[0]) / PPM,
                        (SCREEN_HEIGHT / 2 - screen_coords[1]) / PPM )
    world_coords  = (   window_coords[0] + CAMERA_POSITION[0],
                        window_coords[1] + CAMERA_POSITION[1] )
    return world_coords

if __name__ == '__main__':
    pass
    # TODO: Make a scene for the menu
    # TODO: Load the menu scene here
