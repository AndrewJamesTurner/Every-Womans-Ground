#!/usr/bin/env python3
import ezpygame
from Box2D import b2World, b2PolygonShape
import random
import terraingen
import constants

import shapes
from game import *


class DemoScene(ezpygame.Scene):

    def __init__(self):
        # Called once per game, when game starts

        self.world = b2World()  # default gravity is (0,-10) and doSleep is True

        terrain_raw = terraingen.generate_planet_test(17, round(constants.SCREEN_WIDTH/constants.PPM),
                                                      round(constants.SCREEN_HEIGHT/constants.PPM))
        self.terrain = terraingen.create_terrain(terrain_raw, self.world)

        self.demo_shape = shapes.LLeftShape(self.world, (0, -8))

        # Create an object that moves in the box2d world and can be rendered to the screen

        # A box2d object that doesn't move and isn't rendered to screen
        body_bottom_wall = self.world.CreateStaticBody(
            position=(0 / 2, -5),
            shapes=b2PolygonShape(box=(SCREEN_WIDTH / 2, 5)))

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene
        pass

    def handle_event(self, event):
        # Called every time a pygame event is fired

        # Processing keyboard input here gives one event per key press
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         # Kick the demo shape
        #         #for shape in self.demo_shapes:
        #         #    shape.body.ApplyLinearImpulse((0, 30), shape.body.position, True)
        #         pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Kick a shape
                #kick_shape = self.many_shapes[int(random() * len(self.many_shapes))]
                self.demo_shape.body.ApplyLinearImpulse((0, 100), self.demo_shape.body.position, True)

    def draw(self, screen):
        # Called once per frame, to draw to the screen

        screen.fill(black)
        for block in self.terrain:
            block.draw(screen)
        # for shape in self.demo_shapes:
        #     shape.draw(screen)
        self.demo_shape.draw(screen)

    def update(self, dt):
        # Called once per frame, to update the state of the game

        # Processing keyboard events here lets you track which keys are being held down
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.demo_shape.body.ApplyLinearImpulse((0, 30), self.demo_shape.body.position, True)

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(DemoScene())
