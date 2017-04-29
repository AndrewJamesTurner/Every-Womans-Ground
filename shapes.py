
import constants

from GameObject import *


class LLeftShape(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0, 0], [0.333, 0], [0.333, 0.5], [0, 0.5]], [[0, 0.5], [0.333, 0.5], [0.333, 1], [0, 1]],
                          [[0.333, 0.5], [0.666, 0.5], [0.666, 1], [0.333, 1]], [[0.666, 0.5], [1, 0.5], [1, 1], [0.666, 1]]]
        circle_shapes = []
        image_path = "assets/l_left_shape.png"
        scale = 3

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)


class TerrainBlock(StaticGameObject):

    def __init__(self, world, position, image_fp):
        polygon_points = [[[0, 0], [0, 1], [1, 1], [1, 0]]]
        circle_shapes = []
        scale = 1

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_fp, scale,
                                                   density, friction, restitution)


def terrain_block_factory(biome, position, world):
    return TerrainBlock(world, position, constants.BIOME_TEXTURES[biome])

