
import math

from Box2D import b2CircleShape

from game import *


class GameObject:
    """
    An object that has a box2d representation and a pygame representation.
    Store an instance of this class in the userData of every box2d body that you want to render to the screen.
    """

    # Box2d body for this object
    body = None

    # Image to draw to the screen at this object's position. Can be none, to not draw an image
    image = None

    # Colour in which to render this object's box2d fixtures (mostly for debugging). Can be none, to not render fixtures
    colour = None

    def create(self, world, position):
        raise NotImplementedError

    def draw(self, screen):
        """
        Draw this object to the screen.
        :param screen:
        """
        # Draw box2d collision boxes of body
        if self.colour is not None:
            for fixture in self.body.fixtures:
                shape = fixture.shape
                vertices = [world_to_screen_coordinates(self.body.transform * v) for v in shape.vertices]
                pygame.draw.polygon(screen, self.colour, vertices)

        # Draw image for the body
        if self.image is not None:
            image_rect = self.image.get_rect()
            rotated_image = pygame.transform.rotate(self.image, self.body.angle * 180 / math.pi)
            rotated_image_rect = rotated_image.get_rect(center=world_to_screen_coordinates(self.body.position))
            screen.blit(rotated_image, rotated_image_rect)

    def prepare_shape(self, world, position, polygon_points, circle_shapes, image_path, scale,
                      density=1, friction=0.9, restitution=0.1):
        """
        Convenience function for creating a box2d object and loading an image.
        :param world: box2d world
        :param position: starting coordinates of the object in the box2d world
        :param polygon_points: List of polygons. Each polygon is a list of [x, y] coordinates
        :param circle_shapes: List of circles. Each circle is [xpos, ypos, radius]
        :param image_path: Path to an image file to load and process for this shape
        :param scale: Multiply the polygon_points and circle_shapes numbers by this scale factor
        :param density: box2d physics parameter to set of each created fixture
        :param friction: box2d physics parameter to set of each created fixture
        :param restitution: box2d physics parameter to set of each created fixture
        :return: body, image
        """

        self.scale = scale

        if image_path:
            image = pygame.image.load(image_path).convert_alpha()
            ratio = image.get_height() / image.get_width()
            w, h = int(scale * SHAPE_UNITS_TO_METRES), int(ratio * scale * SHAPE_UNITS_TO_METRES)
            image = pygame.transform.scale(image, (w, h))
        else:
            ratio = 1
            image = None


        # body = world.CreateDynamicBody(position=position)
        body = self.create(world, position)
        body.userData = self

        for polygon in polygon_points:
            polygon = [[scale * (x - 0.5), ratio * scale * ((1 - y) - 0.5)] for x, y in polygon]
            body.CreatePolygonFixture(vertices=polygon, density=density, friction=friction, restitution=restitution)

        for circle in circle_shapes:
            x = scale * circle[0]
            y = ratio * scale * (1 - circle[1])
            r = scale * circle[2]

            circle = b2CircleShape(pos=(x, y), radius=r)
            body.CreateFixture(shape=circle, density=density, friction=friction, restitution=restitution)

        return body, image


class StaticGameObject(GameObject):

    def create(self, world, position):
        return world.CreateStaticBody(position=position)


class DynamicGameObject(GameObject):

    def create(self, world, position):
        return world.CreateDynamicBody(position=position)
