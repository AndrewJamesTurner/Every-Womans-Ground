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

class PlanetScene(GameScene):

    def __init__(self, seed=5):
        super(PlanetScene, self).__init__()

        # Planet defaults
        defs = terrain_utils.default_values

        r = random.Random(seed)
        planet_info = get_space_scene().planet_info

        # TODO Derive planet specific parameters from the higher level values provided!
        # This will include calculations of things like tunnel frequency from number of asteroids in vicinity
        params = defs if planet_info is None else defs

        # Called once per game, when game starts
        terrainblocks.make_blocks(1.0)

        gravity = r.gauss(params['gravity_mean'], params['gravity_sd'])
        self.world = b2World(gravity=(0, gravity), contactListener=EnterLanderListener())

        terrain_raw = terraingen.generate_planet_test(r.random(), 500, 80)

        # Terrain Modifiers
        modifiers = terrain_utils.get_modifiers()
        for modifier in modifiers:
            terrain_raw = modifier(terrain_raw,
                                   params['modifier_params'][modifier.__name__.replace('_modifier', '')],  # Get modifier specific params
                                   r.random())

        init_pos = terraingen.get_initial_position(terrain_raw, 0)
        init_lander = terraingen.get_initial_position(terrain_raw, -10)

        self.terrain = shapes.TerrainBulk(self.world, terrain_raw)
        self.lander = lander_shapes.StationaryLander(self.world, init_lander)
        self.person = shapes.AstronautShape(self.world, init_pos)
        self.person.body.fixedRotation = True
        self.person.body.linearDamping = 0.9

        width, height = self.terrain.terrain.shape
        self.backdrop = shapes.ParallaxBackdrop(-20, os.path.join(ASSETS_PATH, 'backdrop1.jpg'), width )
        self.dustdrop = shapes.ParallaxBackdrop(5, os.path.join(ASSETS_PATH, 'dust.png'), width )

        # TODO Debugging
        self.person_init = init_pos
        self.lander_init = init_lander

        # Level barriers
        self.world.CreateStaticBody(
            position=(0,0),
            shapes=b2PolygonShape(box=(width, 0.5)))
        # A box2d object that doesn't move and isn't rendered to screen
        self.world.CreateStaticBody(
            position=(-width/2, 5*height),
            shapes=b2PolygonShape(box=(0.5, 10*height)))
        self.world.CreateStaticBody(
            position=(width/2, 5*height),
            shapes=b2PolygonShape(box=(0.5, 10*height)))

    def on_enter(self, previous_scene):
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
        cam_x = min(cam_right, max(cam_left, cam_x))

        set_camera_position(cam_x, cam_y)

        screen.fill(black)
        self.backdrop.draw(screen)
        self.dustdrop.draw(screen)
        self.terrain.draw(screen)
        self.person.draw(screen)
        self.lander.draw(screen)

        self.draw_overlays(screen)

    def update(self, dt):
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



class EnterLanderListener(b2ContactListener):

    def BeginContact(self, contact):
        game_object_a = contact.fixtureA.body.userData
        game_object_b = contact.fixtureB.body.userData

        # When landing on a planet, change to the lander scene
        if (isinstance(game_object_a, shapes.AstronautShape) and isinstance(game_object_b, lander_shapes.StationaryLander)) or \
                (isinstance(game_object_a, lander_shapes.StationaryLander) and isinstance(game_object_b, shapes.AstronautShape)):

            global change_to_lander_scene
            change_to_lander_scene = True



if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_planet_scene())
