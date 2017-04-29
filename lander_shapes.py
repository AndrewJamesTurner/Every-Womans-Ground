
from GameObject import *

class Lander(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.39,0], [0.66,0], [1,0.3], [1,0.9], [0,0.9],[0,0.3]]]
        circle_shapes = []
        image_path = "assets/lander.png"
        scale = 2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)

        self.colour = (255,0,0,0)
        self.body.linearDamping = 0.01
        self.body.angularDamping = 0.05

        #Bit hacky - make the sensor box the same as the lander but only the top half(ish) to avoid using the coords system above return from pygame and alter a bit
        #Points 4 and 5 are the bottom, so move the y of these upwards

        # sensorPolygon = self.body.fixtures[0].shape.vertices


        #Add a sensor for collisions1
        #sensor = self.body.CreatePolygonFixture(vertices=polygon)
        #sensor.sensor = True

class StationaryLander(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.39,0], [0.66,0], [1,0.3], [1,0.9], [0,0.9],[0,0.3]]]
        circle_shapes = []
        image_path = "assets/lander.png"
        scale = 2

        density = 20
        friction = 1.0
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)


class PlanetGround(StaticGameObject):

    def __init__(self, world, position, polygonPointArray):

        #Vary this depending on planet status
        density = 1
        friction = 0.5
        restitution = 0.4

        self.body = self.create(world, position)
        self.body.userData = self

        for polygon in polygonPointArray:
            self.body.CreatePolygonFixture(vertices=polygon, density=density, friction=friction, restitution=restitution)

        self.colour = (255,0,0,0)