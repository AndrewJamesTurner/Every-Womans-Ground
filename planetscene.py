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


class PlanetScene(GameScene):

    def __init__(self, seed=5):
        super(PlanetScene, self).__init__()

        # Seed planet
        r = random.Random(seed)

        # Called once per game, when game starts
        terrainblocks.make_blocks(1.0)

        # Randomly generate generate gravity
        # TODO Should gravity have priors for each planet, which are informed by the planets stats as passed in from SpaceScene?
        gravity = r.gauss(-10, 0.05)

        self.world = b2World(gravity=(0, gravity), contactListener=EnterLanderListener())  # default gravity is (0,-10) and doSleep is True

        terrain_raw = terraingen.generate_planet_test(17, 500, 80)

        # Terrain Modifiers
        modifiers = terrain_utils.get_modifiers()
        # TODO Have these values randomly generated from an appropriate distribution (possibly related to a planet's characteristics)

        params = {'tunnel': {
                      'seed': 3,
                      'frequency': 0.05,
                      'depth_mean': 0.3,
                      'depth_sd': 0.05,
                      'width_mean': 2,
                      'width_sd': 0.1
                      },
                  'crater': {
                      'seed': 2,
                      'frequency': 0.02,
                      'radius_mean': 10,
                      'radius_sd': 2,
                  },
                  'vegetation': {
                      'seed': 7,
                      'types':  [
                          {
                          'seedrate':0.8,
                          'root_block':5,
                          'root_depth':1,
                          'grow_block':4,
                          'grow_height':1
                          },
                         {
                        'seedrate':0.1,
                        'root_block':4,
                        'root_depth':2,
                        'grow_block':3,
                        'grow_height':5
                        }
                      ]
                    },
                  'water': {
                      'seed': 12
                     }
                  }

        for modifier in modifiers:
            print("On {}".format(modifier.__name__))
            terrain_raw = modifier(terrain_raw, params[modifier.__name__.replace('_modifier', '')])

        init_pos = terraingen.get_initial_position(terrain_raw, 0)
        init_lander = terraingen.get_initial_position(terrain_raw, -5)

        self.terrain = shapes.TerrainBulk(self.world, terrain_raw)
        self.lander = lander_shapes.StationaryLander(self.world, init_lander)
        self.person = shapes.AstronautShape(self.world, init_pos)
        self.person.body.fixedRotation = True
        self.person.body.linearDamping = 0.9

        width, height = self.terrain.terrain.shape
        self.backdrop = shapes.ParallaxBackdrop(-20, os.path.join(ASSETS_PATH, 'backdrop1.jpg'), width )
        self.dustdrop = shapes.ParallaxBackdrop(5, os.path.join(ASSETS_PATH, 'dust.png'), width )

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
        # Called every time the game switches to this scene
        pass

    def handle_event(self, event):
        # Called every time a pygame event is fired

        # Processing keyboard input here gives one event per key press
        # if event.type == pygame.KEYDOWN:
        #     # Jump!
        #     if event.key == pygame.K_SPACE:
        #         self.person.body.ApplyLinearImpulse((0, PLAYER_JUMP_SPEED), self.person.body.position, True)
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

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()


class EnterLanderListener(b2ContactListener):

    def BeginContact(self, contact):
        game_object_a = contact.fixtureA.body.userData
        game_object_b = contact.fixtureB.body.userData

        # When landing on a planet, change to the lander scene
        if (isinstance(game_object_a, shapes.AstronautShape) and isinstance(game_object_b, lander_shapes.StationaryLander)) or \
                (isinstance(game_object_a, lander_shapes.StationaryLander) and isinstance(game_object_b, shapes.AstronautShape)):

            # TODO Get user input
            print("Do you want to leave the planet?")
            get_planet_scene().application.change_scene(get_lander_scene())



if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_planet_scene())
