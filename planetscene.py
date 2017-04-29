#!/usr/bin/env python3
import ezpygame
from Box2D import b2World, b2PolygonShape
import random

import lander_shapes
import terrain_utils
import terraingen
import constants
import numpy as np

import shapes
from game import *
import random

import terrainblocks

class PlanetScene(ezpygame.Scene):

    def __init__(self):
        # Called once per game, when game starts
        terrainblocks.make_blocks(1.0)

        # Randomly generate generate gravity
        gravity = random.gauss(-10, 0)

        self.world = b2World()  # default gravity is (0,-10) and doSleep is True

        terrain_raw = terraingen.generate_planet_test(17, 500, 80)
        init_pos = terraingen.get_initial_position(terrain_raw, 0)
        init_lander = terraingen.get_initial_position(terrain_raw, -5)

        self.terrain = shapes.TerrainBulk(self.world, terrain_raw)
        self.lander = lander_shapes.StationaryLander(self.world, init_pos)
        self.person = shapes.AstronautShape(self.world, (init_pos[0] - 5, init_pos[1]))
        self.person.body.fixedRotation = True
        self.person_xspeed = 0
        self.person_yspeed = 0
        self.gravity = 1

        # Create an object that moves in the box2d world and can be rendered to the screen

        # A box2d object that doesn't move and isn't rendered to screen
        body_bottom_wall = self.world.CreateStaticBody(
            position=(0, -20),
            shapes=b2PolygonShape(box=(SCREEN_WIDTH / 2, 5)))

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene
        pass

    def handle_event(self, event):
        # Called every time a pygame event is fired

        # Processing keyboard input here gives one event per key press
        if event.type == pygame.KEYDOWN:
            # Jump!
            if event.key == pygame.K_SPACE:
                self.person.body.ApplyLinearImpulse((0, PLAYER_JUMP_SPEED), self.person.body.position, True)

    def draw(self, screen):
        # Called once per frame, to draw to the screen
        set_camera_position(*self.person.body.position)
        screen.fill(black)
        self.terrain.draw(screen)
        self.person.draw(screen)
        self.lander.draw(screen)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Move left and right
        if keys[pygame.K_a]:
            self.person.body.ApplyForce((-constants.PLAYER_MOVEMENT_SPEED, 0), self.person.body.position, True)
        if keys[pygame.K_d]:
            self.person.body.ApplyForce((constants.PLAYER_MOVEMENT_SPEED, 0), self.person.body.position, True)

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_planet_scene())
