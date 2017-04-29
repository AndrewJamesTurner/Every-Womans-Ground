from SpaceShapes import *
import ezpygame
from Box2D import *
from game import *
from GameObject import GameObject
import math
import random


sun = None
planets = None
space_ship = None


class ContactListener(b2ContactListener):

    def BeginContact(self, conctact):

        if isinstance(conctact.fixtureA.body.userData, Planet):
            print(conctact.fixtureA.body.userData.info)

        if isinstance(conctact.fixtureB.body.userData, Planet):
            print(conctact.fixtureB.body.userData.info)

            # change_scene()




class SpaceScene(ezpygame.Scene):


    def __init__(self):
        # Called once per game, when game starts

        global sun
        global planets

        planets = []
        self.planets = []
        self.world = b2World([0,0], contactListener=ContactListener())

        def createPlanet(name, size, type, angular_vel, radius_x, radius_y):
            global planets

            planet = Planet(self.world, (15, 5), size)

            info = {
                "name": name,
                "angular_vel": angular_vel,
                "radius_x": radius_x,
                "radius_y": radius_y,
                "angle": random.random() * 2 * math.pi,
                "type": "rock"
            }

            planet.info = info
            planet.distance_to_sum = 10
            planets.append(planet)
            self.planets.append(planet)


        createPlanet("Earth", 4, "rock", 0.002, 20, 25)
        createPlanet("Mars", 5, "rock", 0.001, 30, 35)
        createPlanet("And", 10, "rock", 0.001, 50, 50)


        space_ship = SpaceShip(self.world, (20, 20))
        self.space_ship = space_ship

        sun = Sun(self.world, (0, 0))
        self.sun = sun

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene
        pass



    def handle_event(self, event):
        # Called every time a pygame event is fired
        pass


    def draw(self, screen):
        # Called once per frame, to draw to thwe screen

        screen.fill(black)
        self.space_ship.draw(screen)

        for planet in self.planets:
            planet.draw(screen)

        self.sun.draw(screen)



    def update(self, dt):
        # Called once per frame, to update the state of the game

        power = 1
        spin = 0.1

        keys = pygame.key.get_pressed()

        xxx = -math.sin(self.space_ship.body.angle)
        yyy = math.cos(self.space_ship.body.angle)

        if keys[pygame.K_SPACE]:
            self.space_ship.body.ApplyLinearImpulse((0, 30), self.space_ship.body.position, True)

        if keys[pygame.K_w]:
            self.space_ship.body.ApplyLinearImpulse((xxx * power, yyy * power), self.space_ship.body.worldCenter, True)

        if keys[pygame.K_d]:
            self.space_ship.body.ApplyAngularImpulse(-spin, True)

        if keys[pygame.K_a]:
            self.space_ship.body.ApplyAngularImpulse(spin, True)


        for planet in self.planets:

            angle = planet.info["angle"]
            radius_x = planet.info["radius_x"]
            radius_y = planet.info["radius_y"]
            angular_vel = planet.info["angular_vel"]


            angle_detla = angular_vel * dt
            angle += angle_detla
            planet.info["angle"] = angle

            planet_position_x = radius_x * math.sin(angle)
            planet_position_y = radius_y * math.cos(angle)

            planet.body.position = (planet_position_x, planet_position_y)


        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()

        set_camera_position(self.space_ship.body.worldCenter[0], self.space_ship.body.worldCenter[1])


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(SpaceScene())
