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
        set_camera_position((SCREEN_WIDTH/PPM)/2,(SCREEN_HEIGHT/PPM)/2)

        #Need to generate a seed
        #Need to set height and xgap based on planet info
        numPoints = 100

        terrain = generate_fractal_heightmap(30, numPoints, int(SCREEN_HEIGHT/PPM)/4, 1)

        #polygons can't have many edges so split into separate polygons
        starty = -100
        pointCountDown = 10
        startCoords = [0,starty]
        xGap = 5

        polygonArray = []
        polygonPoints = [startCoords]

        for index,terrainVal in enumerate(terrain):

            polygonPoints.append([index * xGap, terrainVal])

            if pointCountDown > 0:
                pointCountDown -= 1
            else:
                #finish block and reset counter
                polygonPoints.append([index * xGap, starty])
                polygonArray.append(polygonPoints)

                #Use 9 here because we initialise with two values
                pointCountDown = 9
                polygonPoints = [[index*xGap, starty], [index*xGap, terrainVal]]

        print(polygonArray)

        self.ground = landershapes.PlanetGround(self.world, (0, 0), polygonArray)

        #Add the lander in the middle of the ground
        landerStartHeight = 5
        self.lander = landershapes.Lander(self.world, ((xGap*numPoints)/2, landerStartHeight + (SCREEN_HEIGHT/PPM)/2))

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene
        pass

    def handle_event(self, event):
        # Called every time a pygame event is fired

        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Do something

        pass

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

        xxx = -math.sin(self.lander.body.angle)
        yyy = math.cos(self.lander.body.angle)

        power = 1

        landerPos = self.lander.body.position

        # Processing keyboard input here gives one event per key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.lander.body.angle += 0.01
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.lander.body.angle -= 0.01

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.lander.body.ApplyLinearImpulse((xxx * power, yyy * power), landerPos, True)


        set_camera_position(self.lander.body.position[0],self.lander.body.position[1])

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(LanderScene())
