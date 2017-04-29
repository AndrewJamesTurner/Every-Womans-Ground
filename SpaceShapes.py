from GameObject import GameObject
from game import *
import math


class SpaceShip(GameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.5, 0], [1, 1], [0, 1]]]
        circle_shapes = []
        image_path = "assets/l_left_shape.png"
        scale = 3

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, _ = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        self.colour = red


class Planet(GameObject):

    def __init__(self, world, position):

        def get_point(i, n):
            angle_deg = ((360/n) * i) + (360/n)
            angle_rad = math.pi / 180 * angle_deg

            return [ 0.5 * math.cos(angle_rad) + 0.5, 0.5 * math.sin(angle_rad) + 0.5]

        polygon_points = []
        part = []
        num_points = 16

        for p in range(num_points):
            part.append(get_point(p, num_points))

        polygon_points.append(part)

        print(polygon_points)

        circle_shapes = []
        image_path = "assets/l_left_shape.png"
        scale = 10

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, _ = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        self.colour = white
