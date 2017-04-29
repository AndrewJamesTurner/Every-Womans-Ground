
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

        # May not need sensor - commented out for now
        # #Bit hacky - make the sensor box the same as the lander but only the top half(ish) to avoid using the coords system above return from pygame and alter a bit
        # #Points 3 and 4 are the bottom, so move the y of these upwards
        #
        # sensorPolygonTuples = self.body.fixtures[0].shape.vertices
        # sensorPolygon = []
        # #Change to array from tuple and scale slightly larger than the ship
        # for tuple in sensorPolygonTuples:
        #     point = [tuple[0]*1.1, tuple[1]*1.1]
        #     sensorPolygon.append(point)
        #
        # currentHeight = abs(sensorPolygon[0][1] - sensorPolygon[3][1])
        #
        # #Two lower points are for some reason at 0 and 5
        # sensorPolygon[0][1] = sensorPolygon[0][1] + currentHeight/3
        # sensorPolygon[5][1] = sensorPolygon[5][1] + currentHeight/3
        #
        # #Add a sensor for collisions1
        # self.sensor = self.body.CreatePolygonFixture(vertices=sensorPolygon)
        # self.sensor.sensor = True
        # self.sensor.userData = "LanderCollisionArea"


class StationaryLander(DynamicGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.39,0], [0.66,0], [1,0.3], [1,0.9], [0,0.9],[0,0.3]]]
        circle_shapes = []
        image_path = "assets/lander.png"
        scale = 3

        density = 100
        friction = 1.0
        restitution = 0.4

        self.colour = red

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)


class StationarySpaceship(StaticGameObject):

    def __init__(self, world, position):
        polygon_points = [[[0,0], [1,0.53], [0.06,1]]]
        circle_shapes = []
        image_path = "assets/spaceship-side.png"
        scale = 10

        density = 100
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