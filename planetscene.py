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


class PlanetScene(GameScene):

    def __init__(self, seed=2):
        super(PlanetScene, self).__init__()
        self.seed = seed


    def on_enter(self, previous_scene):

        global change_to_lander_scene
        change_to_lander_scene = False

        # Planet defaults
        defs = terrain_utils.default_values
        params = defs

        if hasattr( get_space_scene(), 'planet_info' ):
            planet_info = get_space_scene().planet_info
            # TODO Derive planet specific parameters from the higher level values provided!
            # This will include calculations of things like tunnel frequency from number of asteroids in vicinity
            r = random.Random(planet_info['seed'])
            params['gravity_mean'] = math.pow(  planet_info['size'], 1.5 )
            archetype = params['type']
            params['modifier_params']['crater']['frequency'] = 0.01 + min(0.2, 2.0 / (0.1 + planet_info['dist_to_asteroid_belt'] ))
        else:
            print(self.seed)
            r = random.Random(self.seed)
            archetypes = list( terrain_utils.terrain_params.keys() )
            archetypes.sort()
            archetype = random.Random(self.seed + 1).choice(archetypes)

        # Called once per game, when game starts
        terrainblocks.make_blocks(1.0)

        tparams = terrain_utils.terrain_params[archetype]

        terrain_seed = r.getrandbits(32)
        modifier_seed = r.getrandbits(32)
        gravity_seed = r.getrandbits(32)
        atmosphere_seed = r.getrandbits(32)
        r_grav  = random.Random(gravity_seed)
        r_atmos = random.Random(atmosphere_seed)

        print(terrain_seed,modifier_seed,gravity_seed,atmosphere_seed)

        gravity = max(0.1, r_grav.gauss(params['gravity_mean'], params['gravity_sd']))
        atmosphere = r_atmos.uniform( *tparams['atmos'] )
        print("%s: g=%f, a=%f" % (archetype, gravity, atmosphere))
        self.world = b2World(gravity=(0, -gravity), contactListener=ContactListener())

        params['modifier_params']['vegetation']['seed_mod'] = 1.0 - abs(atmosphere - 0.5)
        params['modifier_params']['crater']['radius_mean'] = max(6.0, 3.0 / max(0.2, atmosphere))
        params['modifier_params']['tunnel']['width_mean'] = 2.0 * tparams['softness']
        params['modifier_params']['tunnel']['width_sd']   = 0.1 * tparams['softness']

        terrain_raw = terraingen.generate_planet_terrain(terrain_seed, archetype, 500, 80)
        #terrain_raw = terraingen.generate_terrain_test(200, 80)

        # Terrain Modifiers
        modifiers = terrain_utils.get_modifiers()
        for modifier in modifiers:
            terrain_raw = modifier(terrain_raw,
                                   params['modifier_params'][modifier.__name__.replace('_modifier', '')],
                                   # Get modifier specific params
                                   modifier_seed)

        init_pos = terraingen.get_initial_position(terrain_raw, 0)
        init_lander = terraingen.get_initial_position(terrain_raw, -10)

        self.terrain = shapes.TerrainBulk(self.world, terrain_raw)
        self.lander = lander_shapes.StationaryLander(self.world, init_lander)
        self.person = shapes.AstronautShape(self.world, init_pos)


        numFuels = r.randint(0, 10)
        self.fuels = []

        for x in range(0, numFuels):

            xPos = r.randint(-250, 250)
            yPos = terraingen.get_initial_position(terrain_raw, xPos)[1] + 5

            fuel = shapes.FuelShape(self.world, (xPos, yPos))
            fuel.info = {"gameObject": fuel}
            self.fuels.append(fuel)

        numHealths = r.randint(0, 10)
        self.healths = []

        for x in range(0, numFuels):

            xPos = r.randint(-250, 250)
            yPos = terraingen.get_initial_position(terrain_raw, xPos)[1] + 5

            health = shapes.HealthShape(self.world, (xPos, yPos))
            health.info = {"gameObject": health}
            self.healths.append(health)


        self.person.body.fixedRotation = True
        self.person.body.linearDamping = 0.3

        width, height = self.terrain.terrain.shape
        self.backdrop = shapes.ParallaxBackdrop(-20, os.path.join(ASSETS_PATH, 'backdrop1.jpg'), width)
        self.dustdrop = shapes.ParallaxBackdrop(5, os.path.join(ASSETS_PATH, 'dust.png'), width)

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
        self.backdrop.draw(screen)
        self.dustdrop.draw(screen)
        self.terrain.draw(screen)
        self.person.draw(screen)
        self.lander.draw(screen)

        for fuel in self.fuels:
            fuel.draw(screen)

        for health in self.healths:
            health.draw(screen)

        self.draw_overlays(screen)

    def update(self, dt):

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
        if keys[pygame.K_a]:
            self.person.body.ApplyForce((-constants.PLAYER_MOVEMENT_SPEED, 0), self.person.body.position, True)
        if keys[pygame.K_d]:
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
