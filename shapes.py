
import constants

from GameObject import *
import terrainblocks

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


class AstronautShape(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.235, 0.307], [0.235, 0.071], [0.76, 0.071], [0.76, 0.307]],   # Head
                          [[0.21, 0.307], [0.785, 0.307], [0.755, 0.764], [0.235, 0.764]],  # Trunk
                          [[0.5, 0.787], [0.45, 0.933], [0.195, 0.933], [0.35, 0.764]],     # Left leg
                          [[0.5, 0.787], [0.53, 0.933], [0.695, 0.933], [0.645, 0.764]]]    # Right leg
        circle_shapes = []
        image_path = os.path.join(constants.ASSETS_PATH, "astronaut_small.png")

        scale = 2
        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)

class TerrainBlock(StaticGameObject):
    def __init__(self, world, position, blocktype):
        polygon_points = [[[0, 0], [0, 1], [1, 1], [1, 0]]]
        circle_shapes = []

        asset, tint, density, friction, restitution = terrainblocks.BLOCK_DEFS[blocktype]

        self.body, nothing = self.prepare_shape(
            world, position, polygon_points, circle_shapes, None, 1,
            density, friction, restitution )
        self.image = terrainblocks.BLOCK_IMAGES[blocktype]


def terrain_block_factory(blocktype, position, world):
    return TerrainBlock(world, position, blocktype)
