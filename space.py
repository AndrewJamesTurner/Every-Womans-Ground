from SpaceShapes import *
import ezpygame
from Box2D import *
from game import *
from GameObject import GameObject
import math
import random


FIRE_TIMEOUT = 200

to_remove = []


class ContactListener(b2ContactListener):

    def BeginContact(self, contact):
        game_object_a = contact.fixtureA.body.userData
        game_object_b = contact.fixtureB.body.userData

        # When landing on a planet, change to the lander scene
        if (isinstance(game_object_a, Planet) and isinstance(game_object_b, SpaceShip)) or \
                (isinstance(game_object_a, SpaceShip) and isinstance(game_object_b, Planet)):
            # print(conctact.fixtureB.body.userData.info)a

            get_space_scene().planet_info = game_object_b.info

            get_space_scene().application.change_scene(get_lander_scene())

        if isinstance(contact.fixtureA.body.userData, Asteroid) and not isinstance(contact.fixtureB.body.userData, Asteroid):

            if contact.fixtureA not in to_remove:
                to_remove.append(contact.fixtureA)

        if isinstance(contact.fixtureB.body.userData, Asteroid) and not isinstance(contact.fixtureA.body.userData, Asteroid):
            if contact.fixtureB not in to_remove:
                to_remove.append(contact.fixtureB)


class SpaceScene(ezpygame.Scene):

    def createSolarSystem(self, numPlanets, numBelt, position):

        sun = Sun(self.world, position)
        self.suns.append(sun)

        self.createAsteroidBelt(sun, 40, 10)

        planet = self.createPlanet("Earth", 4, "rock", sun, 0.0001, 20, 25, 1)


        self.createPlanet("Mars", 5, "earth", sun, 0.0001, 30, 35, 0)
        self.createPlanet("Andy", 10, "desert", sun, 0.0001, 50, 50, 4)
        self.createPlanet("Andy", 10, "gas", sun, 0.0001, 60, 70, 4)

        self.createAsteroidBelt(sun, 60, 10)


        self.createAsteroid(5, (22,22))


    def createPlanet(self, name, size, ptype, centre, angular_vel, radius_x, radius_y, num_moons):

            planet = Planet(self.world, (15, 5), size, ptype)

            info = {
                "name": name,
                "angular_vel": angular_vel,
                "orbit_radius_x": radius_x,
                "orbit_radius_y": radius_y,
                "orbit_angle": random.random() * 2 * math.pi,
                "type": ptype,
                "orbit_centre": centre,
            }

            planet.info = info
            planet.distance_to_sum = 10
            self.planets.append(planet)

            for i in range(num_moons):
                radius_x = random.randint(size, 3*size);
                radius_y = radius_x + random.randint(0,6) - 3;

                moon = self.createPlanet("Moon", 1, ptype, planet, 0.0005, radius_x, radius_y, 0)

            return planet

    def createAsteroidBelt(self, centre, radius, thickness):

        maxx = 300
        for index in range(maxx):

            angle = 2 * math.pi * index / maxx
            pos_x = centre.body.position[0] + radius * math.sin(angle)
            pos_y = centre.body.position[1] + radius * math.cos(angle) + random.random() * thickness

            bullet = AsteroidBeltBit(self.world, (pos_x, pos_y))

            self.bullets.append(bullet)

        return bullet

    def createAsteroid(self, size, position):

        asteroid = Asteroid(self.world, position, size)

        info = {
            "size": size,
            "gameObject": asteroid
        }

        asteroid.info = info

        self.asteroids.append(asteroid)

        return asteroid

    def __init__(self):
        # Called once per game, when game starts

        self.timeSinceLastFired = 10000
        self.planets = []
        self.bullets = []
        self.asteroids = []
        self.suns = []

        self.world = b2World([0,0], contactListener=ContactListener())

        space_ship = SpaceShip(self.world, (20, 20))
        self.space_ship = space_ship

        self.createSolarSystem(9, 2, (0, 0))


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
        # self.asteroid.draw(screen)

        for planet in self.planets:
            planet.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        for asteroid in self.asteroids:
            asteroid.draw(screen)

        for sun in self.suns:
            sun.draw(screen)

    def update(self, dt):
        # Called once per frame, to update the state of the game

        shared_values = get_shared_values()

        print(shared_values.fuel)

        global to_remove
        to_remove = []

        self.timeSinceLastFired += dt

        power = 1
        spin = 0.1

        keys = pygame.key.get_pressed()

        xxx = -math.sin(self.space_ship.body.angle)
        yyy = math.cos(self.space_ship.body.angle)

        if keys[pygame.K_w]:
            shared_values.fuel -= 1
            self.space_ship.body.ApplyLinearImpulse((xxx * power, yyy * power), self.space_ship.body.worldCenter, True)

        if keys[pygame.K_d]:
            self.space_ship.body.ApplyAngularImpulse(-spin, True)

        if keys[pygame.K_a]:
            self.space_ship.body.ApplyAngularImpulse(spin, True)

        if keys[pygame.K_SPACE]:

            if self.timeSinceLastFired > FIRE_TIMEOUT:

                self.timeSinceLastFired = 0

                bullet = Bullet(self.world, self.space_ship.body.position)

                self.bullets.append(bullet)

                bullet.body.ApplyLinearImpulse((xxx * 100, yyy * 100), bullet.body.worldCenter, True)


        for planet in self.planets:

            angle = planet.info["orbit_angle"]
            radius_x = planet.info["orbit_radius_x"]
            radius_y = planet.info["orbit_radius_y"]
            centre = planet.info["orbit_centre"]
            angular_vel = planet.info["angular_vel"]

            angle_detla = angular_vel * dt
            angle += angle_detla
            planet.info["orbit_angle"] = angle

            planet_position_x = centre.body.position[0] + radius_x * math.sin(angle)
            planet_position_y = centre.body.position[1] + radius_y * math.cos(angle)

            planet.body.position = (planet_position_x, planet_position_y)


        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()

        for remove_me in to_remove:
            if isinstance(remove_me.body.userData, Asteroid):

                info = remove_me.body.userData.info

                new_size = round(info["size"] / 2)

                position = remove_me.body.position

                if info["gameObject"] in self.asteroids:
                    self.asteroids.remove(info["gameObject"])

                self.world.DestroyBody(remove_me.body)

                if new_size >= 1:

                    for i in range(new_size):

                        self.createAsteroid(new_size, (position[0]+random.random()*new_size, position[1]+random.random()*new_size))
                        self.createAsteroid(new_size, (position[0]+random.random()*new_size, position[1]+random.random()*new_size))

        set_camera_position(self.space_ship.body.position[0], self.space_ship.body.position[1])


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_space_scene())
