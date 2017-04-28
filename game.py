
import os

import pygame

from constants import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

pygame.init()


def world_to_screen_coordinates(world_coords):
    return world_coords[0] * PPM, \
           SCREEN_HEIGHT - world_coords[1] * PPM


def screen_to_world_coordinates(screen_coords):
    return screen_coords[0] / PPM, \
           (SCREEN_HEIGHT - screen_coords[1]) / PPM

if __name__ == '__main__':
    pass
    # TODO: Make a scene for the menu
    # TODO: Load the menu scene here
