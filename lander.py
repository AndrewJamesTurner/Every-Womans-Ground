#!/usr/bin/env python3
import ezpygame
from Box2D import b2World, b2PolygonShape

import lander_shapes as landershapes
from game import *
from terraingen import *

from GameObject import *

class LanderScene(ezpygame.Scene):

    def __init__(self):
        # Called once per game, when game starts

        self.world = b2World()  # default gravity is (0,-10) and doSleep is True

        #Set gravity depending on planet type.
        self.world.gravity = (0, -5)

        #Set camera to centre
        set_camera_position((SCREEN_WIDTH/PPM),(SCREEN_HEIGHT/PPM)/2)

        # Create an object that moves in the box2d world and can be rendered to the screen
        self.lander = landershapes.Lander(self.world, (SCREEN_WIDTH/PPM, (SCREEN_HEIGHT/PPM)/2))

        #Need to generate a seed
        terrain = generate_fractal_heightmap(30, 50, int(SCREEN_HEIGHT/PPM)/4, 1)

        #polygons can't have many edges so split into separate polygons
        pointCountDown = 10
        startCoords = [0,0]
        xGap = 2

        polygonArray = []
        polygonPoints = [startCoords]

        for index,terrainVal in enumerate(terrain):

            polygonPoints.append([index * xGap, terrainVal])

            if pointCountDown > 0:
                pointCountDown -= 1
            else:
                #finish block and reset counter
                polygonArray.append(polygonPoints)

                #Use 9 here because we initialise with two values
                pointCountDown = 9
                polygonPoints = [[index*xGap, 0], [index*xGap, terrainVal]]

        self.ground = landershapes.PlanetGround(self.world, (SCREEN_WIDTH / PPM / 2, -5), polygonArray)

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene
        pass

    def handle_event(self, event):
        # Called every time a pygame event is fired

        # Processing keyboard input here gives one event per key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.lander.body.ApplyLinearImpulse((0, 30), self.lander.body.position, True)

    def draw(self, screen):
        # Called once per frame, to draw to the screen

        screen.fill(black)

        self.ground.draw(screen)
        self.lander.draw(screen)

    def update(self, dt):
        # Called once per frame, to update the state of the game

        # Processing keyboard events here lets you track which keys are being held down
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.lander.body.ApplyLinearImpulse((0, 30), self.lander.body.position, True)

        print(self.lander.body.position)
        # print(self.ground.body.position)

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(LanderScene())
