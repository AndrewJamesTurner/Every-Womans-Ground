
import constants

from GameObject import *
import terrainblocks
import numpy
import game

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
        polygon_points = [[[0.051, 0.276], [0.051, 0.004], [0.949, 0.004], [0.949, 0.276]],   # Head
                          [[0.068, 0.802], [0.017, 0.276], [0.992, 0.276], [0.941, 0.802]],  # Trunk
                          [[0.153, 0.996], [0.254, 0.806], [0.5, 0.823], [0.449, 0.996]],     # Left leg
                          [[0.551, 0.996], [0.5, 0.823], [0.754, 0.806], [0.847, 0.996]]]    # Right leg
        circle_shapes = []
        image_path = os.path.join(constants.ASSETS_PATH, "astronaut_small2.png")

        scale = 1
        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)


class FuelShape(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0,0], [0,1], [1,1], [0,1]]]
        circle_shapes = []
        image_path = os.path.join(constants.ASSETS_PATH, "nuclear.png")

        scale = 1
        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)


class HealthShape(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0,0], [0,1], [1,1], [0,1]]]
        circle_shapes = []
        image_path = os.path.join(constants.ASSETS_PATH, "health.png")

        scale = 1
        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)


DEBUG_GRID = 0
class TerrainBulk(StaticGameObject):
    def __init__(self, world, terrain):
        self.bodies = []
        self.terrain = terrain
        width, height = terrain.shape

        for x in range(width):
            for y in range(height):
                blocktype = terrain[x, y]
                if blocktype <= 0:
                    continue
                collisions = 0

                if x==0 or x==width-1:
                    collisions=1
                elif y==0 or y==height-1:
                    collisions=1
                else:
                    for i in numpy.nditer(terrain[x-1:x+2,y-1:y+2]):
                        if i<=0:
                            collisions=1
                            break

                if collisions:
                    coords = (0.5 + x - width/2, 0.5 + y)
                    self.add_block_to_world(world, blocktype, coords)

    def add_block_to_world(self, world, blocktype, position):
        polygon_points = [[[0,0], [0,1], [1,1], [1,0]]]
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
        xmin,ymax = screen_to_world_coordinates((0, 0))
        xmax,ymin = screen_to_world_coordinates((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        xmin += xoffset # Fix up for array
        xmax += xoffset # Fix up for array
        xmin = max(0, math.floor(xmin - 1))
        ymin = max(0, math.floor(ymin - 1))
        xmax = min( width,  1 + math.ceil(xmax + 1) )
        ymax = min( height, 1 + math.ceil(ymax + 1) )
        ox,oy = world_to_screen_coordinates((0.5 + xmin - xoffset, 0.5 + ymin))

        for mask, tiles in [(-128, terrainblocks.WALL_IMAGES), (0, terrainblocks.BLOCK_IMAGES)]:
            rect_x = tiles[1].get_rect(center=(ox,oy))
            for x in range(xmin,xmax):
                rect = rect_x.copy()
                for y in range(ymin,ymax):
                    blocktype = self.terrain[x, y] ^ mask
                    if blocktype > 0:
                        image = tiles[blocktype]
                    else:
                        image = None
                    if image is not None:
                        # Draw image for the body
                        screen.blit(image, rect)
                    rect.move_ip(0, -PPM)
                rect_x.move_ip(PPM, 0)
            # Draw box2d collision boxes of body
            if DEBUG_GRID:
                for b in self.bodies:
                    for fixture in b.fixtures:
                        shape = fixture.shape
                        vertices = [world_to_screen_coordinates(b.transform * v) for v in shape.vertices]
                        pygame.draw.polygon(screen, red, vertices)

class ParallaxBackdrop(StaticGameObject):
    def __init__(self, parallax_factor, image_path, stage_width):
        if image_path:
            width = stage_width * PPM / abs(parallax_factor) + SCREEN_WIDTH
            image = pygame.image.load(image_path).convert_alpha()
            ratio = image.get_height() / image.get_width()
            w, h = int(width), int(ratio * width)
            self.image = pygame.transform.scale(image, (w, h))

            self.parallax_factor = parallax_factor

    def draw(self, screen):
        """
        Draw this object to the screen.
        :param screen:
        """
        # Draw image for the body
        if self.image is not None:
            f = self.parallax_factor
            if f > 0:
                image_rect = self.image.get_rect(
                    midbottom=(
                        SCREEN_WIDTH/2 - PPM * game.CAMERA_POSITION[0]/f,
                        SCREEN_HEIGHT  + PPM * game.CAMERA_POSITION[1]/f) )
            else:
                image_rect = self.image.get_rect(
                    midtop=(
                        SCREEN_WIDTH/2 - PPM * game.CAMERA_POSITION[0]/f,
                        PPM * game.CAMERA_POSITION[1]/f) )
            screen.blit(self.image, image_rect)
