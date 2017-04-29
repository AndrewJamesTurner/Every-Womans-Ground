import ezpygame
import pygame

from constants import *
# from lander import LanderScene
# from menu import MenuScene
# from space import SpaceScene

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

pygame.init()

CAMERA_POSITION = (0, 0)

# Create all the scenes
# menu_scene = MenuScene()
# space_scene = SpaceScene()
# lander_scene = LanderScene()


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
    window_coords = (   (SCREEN_WIDTH  / 2 + screen_coords[0]) / PPM,
                        (SCREEN_HEIGHT / 2 - screen_coords[1]) / PPM )
    world_coords  = (   window_coords[0] + CAMERA_POSITION[0],
                        window_coords[1] + CAMERA_POSITION[1] )
    return world_coords

if __name__ == '__main__':
    app = ezpygame.Application(title="No Woman's Sky", resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(MenuScene())
