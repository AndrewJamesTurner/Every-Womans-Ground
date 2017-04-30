from GameObject import *
from game import *
import math
import random

def get_point(i, n):
            angle_deg = ((360/n) * i) + (360/n)
            angle_rad = math.pi / 180 * angle_deg

            return [ 0.5 * math.cos(angle_rad) + 0.5, 0.5 * math.sin(angle_rad) + 0.5]


class SpaceShip(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.5, 0], [1, 0.8], [1,1], [0,1], [0,0.8]]]
        circle_shapes = []
        image_path = "assets/spaceship.png"
        scale = 5/2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        # self.colour = red


class Bullet(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0,0], [1,0], [1,1], [0,1]]]
        circle_shapes = []
        image_path = None
        scale = 0.5/2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, _ = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        self.colour = white


class AsteroidBeltBit(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0,0], [1,0], [1,1], [0,1]]]
        circle_shapes = []
        image_path = None
        scale = 0.5/2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, _ = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        self.colour = white



class Asteroid(DynamicGameObject):

    def __init__(self, world, position, scale):

        polygon_points = []
        part = []
        num_points = 16

        for p in range(num_points):
            point = get_point(p, num_points)

            point[0] += 0.4 * random.random() - 0.8
            point[1] += 0.4 * random.random() - 0.8

            part.append(point)

        polygon_points.append(part)

        circle_shapes = []
        image_path = None
        scale = scale/2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, _ = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        self.colour = grey


class Planet(StaticGameObject):

    def __init__(self, world, position, scale, ptype):

        polygon_points = []
        part = []
        num_points = 16

        for p in range(num_points):
            part.append(get_point(p, num_points))

        polygon_points.append(part)

        circle_shapes = []

        rock_images = [
            "assets/moon.png",
        ]

        desert_images = [
            "assets/mars.png",
            "assets/mars2.png",
            "assets/mars3.png",
            "assets/venus.png",
            "assets/venus2.png",
        ]

        earth_images = [
            "assets/world.png",
        ]

        other_images = [
            "assets/oddPlanet.png",
        ]

        ice_images = [
            "assets/uranus.png",
        ]

        gas_images = [
            "assets/planet.png",
            "assets/uranus.png",
        ]


        if ptype == "rock":
            image_path = random.choice(rock_images)
        elif ptype == "earth":
            image_path = random.choice(earth_images)
        elif ptype == "desert":
            image_path = random.choice(desert_images)
        elif ptype == "gas":
            image_path = random.choice(gas_images)
        elif ptype == "ice":
            image_path = random.choice(ice_images)
        else:
            image_path = random.choice(other_images)


        scale = scale/2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        # self.colour = white



class Sun(StaticGameObject):

    def __init__(self, world, position, size):

        polygon_points = []
        part = []
        num_points = 16

        for p in range(num_points):
            part.append(get_point(p, num_points))

        polygon_points.append(part)

        circle_shapes = []
        image_path = "assets/sun.png"
        scale = size/2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
        # self.colour = yellow
