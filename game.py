#!/usr/bin/env python3
import ezpygame
import pygame

from constants import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

pygame.init()

CAMERA_POSITION = (0, 0)


def set_camera_position(x,y):
    global CAMERA_POSITION
    CAMERA_POSITION = (x, y)


def world_to_screen_coordinates(world_coords):
    window_coords = (   world_coords[0] - CAMERA_POSITION[0],
                        world_coords[1] - CAMERA_POSITION[1] )
    screen_coords = (   SCREEN_WIDTH  / 2 + window_coords[0] * PPM,
                        SCREEN_HEIGHT / 2 - window_coords[1] * PPM )
    return screen_coords

def screen_to_world_coordinates(screen_coords):
    window_coords = (   (screen_coords[0] - SCREEN_WIDTH / 2) / PPM,
                        (SCREEN_HEIGHT / 2 - screen_coords[1]) / PPM )
    world_coords  = (   window_coords[0] + CAMERA_POSITION[0],
                        window_coords[1] + CAMERA_POSITION[1] )
    return world_coords

# Scenes
menu_scene = None
space_scene = None
lander_scene = None
planet_scene = None
game_over_scene = None

def get_menu_scene():
    global menu_scene
    if menu_scene is None:
        from menu import MenuScene
        menu_scene = MenuScene()
    return menu_scene

def get_space_scene():
    global space_scene
    if space_scene is None:
        from space import SpaceScene
        space_scene = SpaceScene()
    return space_scene

def get_lander_scene():
    global lander_scene
    if lander_scene is None:
        from lander import LanderScene
        lander_scene = LanderScene()
    return lander_scene

def get_planet_scene():
    global planet_scene
    if planet_scene is None:
        from planetscene import PlanetScene
        planet_scene = PlanetScene()
    return planet_scene

def get_game_over_scene():
    global game_over_scene
    if game_over_scene is None:
        from GameOverScene import GameOverScene
        game_over_scene = GameOverScene()
    return game_over_scene

# Values shared by every scene
shared_values = None

class SharedValues:

    import constants

    health = constants.MAX_HEALTH
    fuel = constants.MAX_FUEL
    oxygen = constants.MAX_OXYGEN

def get_shared_values():
    global shared_values
    if shared_values is None:
        shared_values = SharedValues()
    return shared_values

if __name__ == '__main__':
    from menu import MenuScene
    app = ezpygame.Application(title="Every Woman's Ground", resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_menu_scene())
