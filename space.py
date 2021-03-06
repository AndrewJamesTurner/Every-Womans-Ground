from SpaceShapes import *
import ezpygame
from Box2D import *
from game import *
from GameObject import GameObject
from GameScene import GameScene
import math
import random
import shapes


ptypes = ["rock", "earth", "desert", "gas", "other", "ice"]
FIRE_TIMEOUT = 200
to_remove = []


change_to_lander_scene = False

class ContactListener(b2ContactListener):

    def BeginContact(self, contact):
        game_object_a = contact.fixtureA.body.userData
        game_object_b = contact.fixtureB.body.userData

        # When landing on a planet, change to the lander scene
        if (isinstance(game_object_a, Planet) and isinstance(game_object_b, SpaceShip)) or \
                (isinstance(game_object_a, SpaceShip) and isinstance(game_object_b, Planet)):

            get_space_scene().planet_info = game_object_b.info

            global change_to_lander_scene
            change_to_lander_scene = True


        if isinstance(contact.fixtureA.body.userData, Asteroid) and not isinstance(contact.fixtureB.body.userData, Asteroid):
            if contact.fixtureA not in to_remove:
                to_remove.append(contact.fixtureA)

        if isinstance(contact.fixtureB.body.userData, Asteroid) and not isinstance(contact.fixtureA.body.userData, Asteroid):
            if contact.fixtureB not in to_remove:
                to_remove.append(contact.fixtureB)


        if (isinstance(contact.fixtureB.body.userData, Sun) and isinstance(contact.fixtureA.body.userData, SpaceShip)) or (isinstance(contact.fixtureA.body.userData, Sun) and isinstance(contact.fixtureB.body.userData, SpaceShip)):
            get_shared_values().health = 0

        if (isinstance(contact.fixtureB.body.userData, SpaceShip) and not isinstance(contact.fixtureA.body.userData, Planet)) or (isinstance(contact.fixtureA.body.userData, SpaceShip) and not isinstance(contact.fixtureB.body.userData, Planet)):

            velocity1 = contact.fixtureA.body.linearVelocity
            velocity2 = contact.fixtureA.body.linearVelocity

            speed1 = math.sqrt(pow(velocity1[0], 2) + pow(velocity1[0], 2))
            speed2 = math.sqrt(pow(velocity2[0], 2) + pow(velocity2[0], 2))

            speed = max(speed1, speed2)

            get_shared_values().health -= speed/10



class SpaceScene(GameScene):

    def createSolarSystem(self, numPlanets, numBelt, numAsteroids, position):

        self.r = random.Random(random.getrandbits(32))

        size = self.r.randint(20, 50)
        sun = Sun(self.world, position, size)
        self.suns.append(sun)

        x_radius = self.r.randint(size, size+20)

        asteroidBeltRadiuseseses = []

        for x in range(numBelt):

            radius = self.r.randint(20, 100)
            width = self.r.randint(5, 20)
            dencity = self.r.randint(100, 200)

            self.createAsteroidBelt(sun, radius, width, dencity)
            asteroidBeltRadiuseseses.append(radius)

        for x in range(numPlanets):
            # TODO: Weight some of the parameters based on ptype
            size = self.r.randint(5, 15)
            ptype = self.r.choice(ptypes)
            x_radius += self.r.randint(5, 20)
            angle_vel = self.r.randint(10, 50) * 0.01 / (x_radius * x_radius)
            y_radius = x_radius + self.r.randint(0,  x_radius) - x_radius/2;
            num_moons = self.r.randint(0, 4)

            dist_to_asteroid_belt = 1000000
            for a in asteroidBeltRadiuseseses:

                if abs(x_radius - a) < dist_to_asteroid_belt:
                    dist_to_asteroid_belt = abs(x_radius - a)

            planet = self.createPlanet("Andy", size, ptype, sun, angle_vel, x_radius, y_radius, num_moons, dist_to_asteroid_belt)



    def createPlanet(self, name, size, ptype, orbit_centre, angular_vel, radius_x, radius_y, num_moons, dist_to_asteroid_belt):

            planet = Planet(self.world, size, ptype)

            info = {
                "name": name,
                "size": size,
                "angular_vel": angular_vel,
                "orbit_radius_x": radius_x,
                "orbit_radius_y": radius_y,
                "orbit_angle": self.r.random() * 2 * math.pi,
                "type": ptype,
                "orbit_centre": orbit_centre,
                "seed": self.r.getrandbits(32),
                "dist_to_asteroid_belt": dist_to_asteroid_belt,
            }

            planet.info = info
            self.planets.append(planet)

            for i in range(num_moons):
                radius_x = self.r.randint(size, 3 * size);
                radius_y = radius_x + self.r.randint(0,6) - 3;
                size = self.r.randint(2, size);
                # TODO: Randomly choose mtype based on ptype using some weighting system
                mtype=ptype
                self.createPlanet("Moon", size, mtype, planet, 0.0005, radius_x, radius_y, 0, dist_to_asteroid_belt)

            return planet

    def createAsteroidBelt(self, centre, radius, thickness, dencity):


        for index in range(dencity):

            angle = 2 * math.pi * index / dencity
            pos_x = centre.body.position[0] + radius * math.sin(angle) + self.r.random() * thickness
            pos_y = centre.body.position[1] + radius * math.cos(angle) + self.r.random() * thickness

            if self.r.random() < 0.10:
                size = self.r.randint(1, 5)
                self.createAsteroid(size, (pos_x,pos_y))
            else:
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
        super(SpaceScene, self).__init__()

        # Called once per game, when game starts




    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        global change_to_lander_scene
        change_to_lander_scene = False

        self.planet_info = None
        self.timeSinceLastFired = 10000
        self.planets = []
        self.bullets = []
        self.asteroids = []
        self.suns = []

        self.world = b2World([0, 0], contactListener=ContactListener())

        space_ship = SpaceShip(self.world, (20, 20))
        self.space_ship = space_ship

        self.createSolarSystem(9, 2, 50, (0, 0))
        # self.createSolarSystem(12, 3, 50, (100, 100))

        self.arrow_imamge = pygame.image.load("assets/arrow.png").convert_alpha()
        image_rect = self.arrow_imamge.get_rect()
        self.arrow_imamge = pygame.transform.smoothscale(self.arrow_imamge,
                                                         (int(0.2 * image_rect[2]), int(0.2 * image_rect[2])))

#        self.backdrop = shapes.ParallaxBackdrop(100, os.path.join(ASSETS_PATH, 'sky.png'), width)

        get_shared_values().oxygen = MAX_OXYGEN


    def handle_event(self, event):
        # Called every time a pygame event is fired
        pass


    def draw(self, screen):
        # Called once per frame, to draw to thwe screen

        screen.fill((0x30,0x00,0x60,0xff))

#        self.backdrop.draw(screen)


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

        ship_position = self.space_ship.body.position
        nearest_planet_position = None
        nearest_planet_dist = 100000


        def distance(posA, posB):

            dx = abs(posA[0] - posB[0])
            dy = abs(posA[1] - posB[1])

            return math.sqrt(dx*dx + dy*dy)


        for planet in self.planets:

            planet_position = planet.body.position
            dist = distance(ship_position, planet_position)

            if dist < nearest_planet_dist:
                nearest_planet_dist = dist
                nearest_planet_position = planet_position


        def angle(posA, posB):

            dx = (posA[0] - posB[0])
            dy = (posA[1] - posB[1])

            return math.atan2(dy, dx)


        # print(angle(ship_position, nearest_planet_position))
        # print(nearest_planet_dist)

        # direction = (ship_position[0] - nearest_planet_position[0], ship_position[1] - nearest_planet_position[1])
        # aaa = math.atan2(direction[1], direction[0])

        image_rect = self.arrow_imamge.get_rect()
        rotated_image = pygame.transform.rotate(self.arrow_imamge, angle(ship_position, nearest_planet_position)* 180 / math.pi  + 90 )
        # rotated_image = pygame.transform.rotate(self.arrow_imamge, self.space_ship.body.angle * 180 / math.pi)

        image_rect[0] = SCREEN_WIDTH - 100
        image_rect[1] = SCREEN_HEIGHT - 100
        # rotated_image_rect = rotated_image.get_rect(center=world_to_screen_coordinates(self.body.position))
        screen.blit(rotated_image, image_rect)

        self.draw_overlays(screen)

    def update(self, dt):
        # Called once per frame, to update the state of the game
        global to_remove
        to_remove = []

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

                        self.createAsteroid(new_size, (position[0]+self.r.random()*new_size, position[1]+self.r.random()*new_size))
                        self.createAsteroid(new_size, (position[0]+self.r.random()*new_size, position[1]+self.r.random()*new_size))

        global change_to_lander_scene
        if change_to_lander_scene:
            self.application.change_scene(get_lander_scene())

        shared_values = get_shared_values()

        # print(shared_values.fuel)

        self.timeSinceLastFired += dt

        power = 2
        spin = 0.3

        keys = pygame.key.get_pressed()

        xxx = -math.sin(self.space_ship.body.angle)
        yyy = math.cos(self.space_ship.body.angle)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            shared_values.fuel -= 1
            self.space_ship.body.ApplyLinearImpulse((xxx * power, yyy * power), self.space_ship.body.worldCenter, True)

        if keys[pygame.K_e]:
            shared_values.fuel -= 100
            self.space_ship.body.ApplyLinearImpulse((xxx * power*10, yyy * power*10), self.space_ship.body.worldCenter, True)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.space_ship.body.ApplyAngularImpulse(-spin, True)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.space_ship.body.ApplyAngularImpulse(spin, True)

        if keys[pygame.K_ESCAPE]:
            exit()

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

        set_camera_position(self.space_ship.body.position[0], self.space_ship.body.position[1])

        self.check_game_over()


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_space_scene())
