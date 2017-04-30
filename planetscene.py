#!/usr/bin/env python3
from Box2D import b2World, b2PolygonShape, b2ContactListener

import lander_shapes
import terrain_utils
import terraingen
import constants

import shapes
from game import *
from GameScene import GameScene
import random
import terrainblocks

change_to_lander_scene = False

to_remove = []


class DataBox:

    def __init__(self):

        self.oxygen = None
        self.water = None
        self.gravity = None
        self.tempurature = None

        font_size = 24
        self.font = pygame.font.Font("assets/TitilliumWeb-Regular.ttf", font_size)

    def draw(self, screen):

        width = 240
        height = 160
        line_height = 30
        offset = 18

        screenImage = pygame.image.load("assets/display.png")
        screenImage = pygame.transform.smoothscale(screenImage, (width,height))
        screen.blit(screenImage, (SCREEN_WIDTH-width*1.05 - offset, SCREEN_HEIGHT-height*1.05 - offset))

        text = "Oxygen: " + ("???" if self.oxygen is None else "{:.1f}".format(self.oxygen*100) + "%")
        text_surface = self.font.render(text, True, black)
        screen.blit(text_surface, (SCREEN_WIDTH-width*1.05, SCREEN_HEIGHT-height*1.07))

        text = "Gravity: " + ("???" if self.gravity is None else  "{:.1f}".format(self.gravity) + " m/s/s")
        text_surface = self.font.render(text, True, black)
        screen.blit(text_surface, (SCREEN_WIDTH-width*1.05, SCREEN_HEIGHT-height*1.07+line_height))

        text = "Water: " + ("???" if self.water is None else ("Yes" if self.water else "No"))
        text_surface = self.font.render(text, True, black)
        screen.blit(text_surface, (SCREEN_WIDTH-width*1.05, SCREEN_HEIGHT-height*1.07+2*line_height))

        text = "Tempurature: " + ("???" if self.tempurature is None else "{:.0f}".format(self.tempurature) + " K")
        text_surface = self.font.render(text, True, black)
        screen.blit(text_surface, (SCREEN_WIDTH-width*1.05, SCREEN_HEIGHT-height*1.07+3*line_height))

    def is_new_home(self):

        min_oxygen = 0.15
        max_oxygen = 0.25

        min_gravity = 8
        max_gravity = 12

        min_temp = 280
        max_temp = 310

        if self.oxygen is None or self.oxygen < min_oxygen or self.oxygen > max_oxygen:
            return False
        elif not self.water:
            return False
        elif self.gravity is None or self.gravity < min_gravity or self.gravity > max_gravity:
            return False
        elif self.tempurature is None or self.tempurature < min_temp or self.tempurature > max_temp:
            return False
        else:
            return True


class PlanetScene(GameScene):

    def __init__(self, seed=15):
        super(PlanetScene, self).__init__()

        self.seed = seed

    def on_enter(self, previous_scene):

        global change_to_lander_scene
        change_to_lander_scene = False

        self.data_box = DataBox()
        self.time_on_planet = 0

        if hasattr( get_space_scene(), 'planet_info' ):
            planet_info = get_space_scene().planet_info
            r = random.Random(planet_info['seed'])
            archetype = planet_info['type']
        else: ### DEBUGGING ONLY
            print(self.seed)
            r = random.Random(self.seed)
            archetypes = list( terrain_utils.terrain_params.keys() )
            archetypes.sort()
            archetype = random.Random(self.seed + 1).choice(archetypes)
            planet_info = None

        # Called once per game, when game starts
        terrainblocks.make_blocks(1.0)

        terrain_seed = r.getrandbits(32)
        modifier_seed = r.getrandbits(32)

        # Load planet specific params
        self.params = terrain_utils.get_planet_params(archetype, planet_info)

        print(terrain_seed,modifier_seed)
        print("%s: g=%f, a=%f" % (archetype, self.params['gravity'], self.params['atmosphere']))

        self.world = b2World(gravity=(0, -self.params['gravity']), contactListener=ContactListener())

        terrain_raw = terraingen.generate_planet_terrain(terrain_seed, archetype, 500)

        # Terrain Modifiers
        modifiers = terrain_utils.get_modifiers()
        for modifier in modifiers:
            terrain_raw = modifier(terrain_raw,
                                   self.params['modifier_params'][modifier.__name__.replace('_modifier', '')],
                                   # Get modifier specific params
                                   modifier_seed)

        init_pos = terraingen.get_initial_position(terrain_raw, 10, 2)
        init_lander = terraingen.get_initial_position(terrain_raw, -10, 5)

        self.terrain = shapes.TerrainBulk(self.world, terrain_raw)
        self.lander = lander_shapes.StationaryLander(self.world, init_lander)
        self.person = shapes.AstronautShape(self.world, init_pos)

        numFuels = r.randint(0, 10)
        self.fuels = []

        for x in range(0, numFuels):

            xPos = r.randint(-250, 250)
            pos = terraingen.get_initial_position(terrain_raw, xPos, 5)

            fuel = shapes.FuelShape(self.world, pos)
            fuel.info = {"gameObject": fuel}
            self.fuels.append(fuel)

        numHealths = r.randint(0, 10)
        self.healths = []

        for x in range(0, numFuels):

            xPos = r.randint(-250, 250)
            pos = terraingen.get_initial_position(terrain_raw, xPos, 5)

            health = shapes.HealthShape(self.world, pos)
            health.info = {"gameObject": health}
            self.healths.append(health)


        self.person.body.fixedRotation = True
        self.person.body.linearDamping = 0.3

        width, height = self.terrain.terrain.shape
        self.backdrop = shapes.ParallaxBackdrop(10, os.path.join(ASSETS_PATH, 'planets', archetype + '.png'), width)
        self.skydrop = shapes.ParallaxBackdrop(-20, os.path.join(ASSETS_PATH, 'backdrop1.jpg'), width)

        # TODO Debugging
        self.person_init = init_pos
        self.lander_init = init_lander

        # Level barriers
        self.world.CreateStaticBody(
            position=(0, 0),
            shapes=b2PolygonShape(box=(width, 0.5)))
        # A box2d object that doesn't move and isn't rendered to screen
        self.world.CreateStaticBody(
            position=(-width / 2, 5 * height),
            shapes=b2PolygonShape(box=(0.5, 10 * height)))
        self.world.CreateStaticBody(
            position=(width / 2, 5 * height),
            shapes=b2PolygonShape(box=(0.5, 10 * height)))

        self.lander.body.position = self.lander_init
        self.person.body.position = self.person_init

    def handle_event(self, event):
        # Called every time a pygame event is fired
        pass

    def draw(self, screen):
        # Called once per frame, to draw to the screen
        cam_x, cam_y = self.person.body.position

        width, height = self.terrain.terrain.shape
        halfwidth = SCREEN_WIDTH / 2 / PPM
        cam_right = width/2 - halfwidth
        cam_left  = -cam_right
        cam_base  = SCREEN_HEIGHT / 2 / PPM
        cam_x = min(cam_right, max(cam_left, cam_x))
        cam_y = max(cam_base, cam_y)

        set_camera_position(cam_x, cam_y)

        screen.fill(black)
        self.skydrop.draw(screen)
        self.backdrop.draw(screen)
        self.terrain.draw(screen)
        self.person.draw(screen)
        self.lander.draw(screen)

        for fuel in self.fuels:
            fuel.draw(screen)

        for health in self.healths:
            health.draw(screen)

        self.data_box.draw(screen)

        self.draw_overlays(screen)

    def update(self, dt):

        self.update_rng = random.Random()
        self.time_on_planet += dt
        get_shared_values().oxygen -= (dt / 100)

        global to_remove
        to_remove = []

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()

        global change_to_lander_scene
        if change_to_lander_scene:
            get_planet_scene().application.change_scene(get_lander_scene())

        keys = pygame.key.get_pressed()

        if get_shared_values().fuel <= 0:
            print("GAME OVER!")
            # TODO Close to game over screen

        # Move left and right
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.person.body.ApplyForce((-constants.PLAYER_MOVEMENT_SPEED, 0), self.person.body.position, True)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.person.body.ApplyForce((constants.PLAYER_MOVEMENT_SPEED, 0), self.person.body.position, True)

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.person.body.ApplyLinearImpulse((0, constants.JETPACK_THRUST), self.person.body.position, True)
            get_shared_values().fuel -= constants.JETPACK_FUEL_USAGE

        if keys[pygame.K_ESCAPE]:
            exit()

        for remove_me in to_remove:

            info = remove_me.body.userData.info

            if info["gameObject"] in self.fuels:
                    self.fuels.remove(info["gameObject"])

            if info["gameObject"] in self.healths:
                    self.healths.remove(info["gameObject"])

            self.world.DestroyBody(remove_me.body)


        self.check_game_over()
        self.check_shared_values()

        for t in range(dt):

            if self.update_rng.random() < 0.0001 and not self.data_box.oxygen:
                self.data_box.oxygen = self.params["oxygen"]
                pass

            if self.update_rng.random() < 0.0001 and not self.data_box.water:
                self.data_box.water = self.params["water"]
                pass

            if self.update_rng.random() < 0.0001 and not self.data_box.tempurature:
                self.data_box.tempurature = self.params["temp"]
                pass

            if self.update_rng.random() < 0.0001 and not self.data_box.gravity:
                self.data_box.gravity = self.params["gravity"]

        if self.data_box.is_new_home():
            self.application.change_scene(get_win_scene())



class ContactListener(b2ContactListener):

    def BeginContact(self, contact):

        global to_remove

        game_object_a = contact.fixtureA.body.userData
        game_object_b = contact.fixtureB.body.userData

        game_fixture_a = contact.fixtureA
        game_fixture_b = contact.fixtureB

        # When landing on a planet, change to the lander scene
        if (isinstance(game_object_a, shapes.AstronautShape) and isinstance(game_object_b, lander_shapes.StationaryLander)) or \
                (isinstance(game_object_a, lander_shapes.StationaryLander) and isinstance(game_object_b, shapes.AstronautShape)):

            global change_to_lander_scene
            change_to_lander_scene = True


        if isinstance(game_object_a, shapes.FuelShape) and isinstance(game_object_b, shapes.AstronautShape):
            if game_fixture_a not in to_remove:
                to_remove.append(game_fixture_a)
                get_shared_values().fuel += 1000


        if isinstance(game_object_b, shapes.FuelShape) and isinstance(game_object_a, shapes.AstronautShape):
            if game_fixture_b not in to_remove:
                to_remove.append(game_fixture_b)
                get_shared_values().fuel += 1000


        if isinstance(game_object_a, shapes.HealthShape) and isinstance(game_object_b, shapes.AstronautShape):
            if game_fixture_a not in to_remove:
                to_remove.append(game_fixture_a)
                get_shared_values().health += 100


        if isinstance(game_object_b, shapes.HealthShape) and isinstance(game_object_a, shapes.AstronautShape):
            if game_fixture_b not in to_remove:
                to_remove.append(game_fixture_b)
                get_shared_values().health += 100


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_planet_scene())
