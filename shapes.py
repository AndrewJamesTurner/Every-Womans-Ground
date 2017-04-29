
import constants

from GameObject import *
import terrainblocks
import numpy

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
        self.colour=red

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)

class TerrainBulk(StaticGameObject):
    def __init__(self, world, terrain):
        self.bodies = []
        self.terrain = terrain
        width, height = terrain.shape

        for x in range(width):
            for y in range(height):
                blocktype = terrain[x, y]
                if not blocktype:
                    continue
                collisions = 0

                if x==0 or x==width-1:
                    collisions=1
                elif y==0 or y==height-1:
                    collisions=1
                else:
                    for i in numpy.nditer(terrain[x-1:x+2,y-1:y+2]):
                        if i==0:
                            collisions=1
                            break

                if collisions:
                    coords = (0.5 + x - width/2, 0.5 + y)
                    self.add_block_to_world(world, blocktype, coords)

    def add_block_to_world(self, world, blocktype, position):
        polygon_points = [[[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]]
        asset, tint, density, friction, restitution = terrainblocks.BLOCK_DEFS[blocktype]

        body, nothing = self.prepare_shape(
            world, position, polygon_points, [], None, 1,
            density, friction, restitution )
        self.bodies.append(body)

    def draw(self, screen):
        """
        Draw this object to the screen.
        :param screen:
        """
        width, height = self.terrain.shape
        xoffset = width / 2
        for x in range(width):
            for y in range(height):
                blocktype = self.terrain[x, y]
                image = terrainblocks.BLOCK_IMAGES[blocktype]
                if image is None:
                    continue
                # Draw image for the body
                image_rect = image.get_rect(center=world_to_screen_coordinates((0.5 + x - xoffset, 0.5 + y)))
                screen.blit(image, image_rect)
