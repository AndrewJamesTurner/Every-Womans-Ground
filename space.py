from SpaceShapes import *
import ezpygame
from Box2D import *
from game import *
from GameObject import GameObject
import math
import random





class ContactListener(b2ContactListener):

    def BeginContact(self, conctact):

        if isinstance(conctact.fixtureA.body.userData, Planet):
            print(conctact.fixtureA.body.userData.info)

        if isinstance(conctact.fixtureB.body.userData, Planet):
            print(conctact.fixtureB.body.userData.info)

            # space_scene.applicatiochange_scene(lander_scene)




class SpaceScene(ezpygame.Scene):


    def __init__(self):
        # Called once per game, when game starts

        planets = []
        self.planets = []
        self.bullets = []

        self.world = b2World([0,0], contactListener=ContactListener())

        def createAsteroidBelt(centre, radius, thickness):

            maxx = 300
            for index in range(maxx):

                angle = 2 * math.pi * index / maxx
                pos_x = centre.body.position[0] + radius * math.sin(angle)
                pos_y = centre.body.position[1] + radius * math.cos(angle) + random.random() * thickness

                bullet = Bullet(self.world, (pos_x, pos_y))

                self.bullets.append(bullet)


        def createPlanet(name, size, type, centre, angular_vel, radius_x, radius_y):

            planet = Planet(self.world, (15, 5), size)

            info = {
                "name": name,
                "angular_vel": angular_vel,
                "radius_x": radius_x,
                "radius_y": radius_y,
                "angle": random.random() * 2 * math.pi,
                "type": "rock",
                "centre": centre,
            }

            planet.info = info
            planet.distance_to_sum = 10
            planets.append(planet)
            self.planets.append(planet)

            return planet


        space_ship = SpaceShip(self.world, (20, 20))
        self.space_ship = space_ship

        sun = Sun(self.world, (0, 0))
        self.sun = sun

        createAsteroidBelt(sun, 40, 10)

        planet = createPlanet("Earth", 4, "rock", sun, 0.001, 20, 25)
        moon = createPlanet("Moon", 1, "rock", planet, 0.005, 6, 6)


        createPlanet("Mars", 5, "rock", sun, 0.001, 30, 35)
        createPlanet("Andy", 10, "rock", sun, 0.001, 50, 50)

        self.asteroid = Asteroid(self.world, (22, 22), 2)



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
        self.asteroid.draw(screen)

        for planet in self.planets:
            planet.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        self.sun.draw(screen)



    def update(self, dt):
        # Called once per frame, to update the state of the game

        power = 1
        spin = 0.1

        keys = pygame.key.get_pressed()

        xxx = -math.sin(self.space_ship.body.angle)
        yyy = math.cos(self.space_ship.body.angle)

        if keys[pygame.K_w]:
            self.space_ship.body.ApplyLinearImpulse((xxx * power, yyy * power), self.space_ship.body.worldCenter, True)

        if keys[pygame.K_d]:
            self.space_ship.body.ApplyAngularImpulse(-spin, True)

        if keys[pygame.K_a]:
            self.space_ship.body.ApplyAngularImpulse(spin, True)

        if keys[pygame.K_SPACE]:

            bullet = Bullet(self.world, self.space_ship.body.position)

            self.bullets.append(bullet)

            bullet.body.ApplyLinearImpulse((xxx * 100, yyy * 100), bullet.body.worldCenter, True)


        for planet in self.planets:

            angle = planet.info["angle"]
            radius_x = planet.info["radius_x"]
            radius_y = planet.info["radius_y"]
            centre = planet.info["centre"]
            angular_vel = planet.info["angular_vel"]

            angle_detla = angular_vel * dt
            angle += angle_detla
            planet.info["angle"] = angle

            planet_position_x = centre.body.position[0] + radius_x * math.sin(angle)
            planet_position_y = centre.body.position[1] + radius_y * math.cos(angle)

            planet.body.position = (planet_position_x, planet_position_y)


        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()

        set_camera_position(self.space_ship.body.position[0], self.space_ship.body.position[1])


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(SpaceScene())
