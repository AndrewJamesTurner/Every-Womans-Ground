from SpaceShapes import *
import ezpygame
from Box2D import b2World, b2PolygonShape

from game import *
from GameObject import GameObject
import math


class SpaceScene(ezpygame.Scene):

    def __init__(self):
        # Called once per game, when game starts

        self.world = b2World([0,0])  # default gravity is (0,-10) and doSleep is True

        # Create an object that moves in the box2d world and can be rendered to the screen
        self.space_ship = SpaceShip(self.world, (5, 5))
        self.planet = Planet(self.world, (10, 5))

        # A box2d object that doesn't move and isn't rendered to screen
        # body_bottom_wall = self.world.CreateStaticBody(
        #     position=(SCREEN_WIDTH / 2, -5),
        #     shapes=b2PolygonShape(box=(SCREEN_WIDTH / 2, 5)))


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
        self.planet.draw(screen)



    def update(self, dt):
        # Called once per frame, to update the state of the game

        # Processing keyboard events here lets you track which keys are being held down
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.space_ship.body.ApplyLinearImpulse((0, 30), self.space_ship.body.position, True)
        power = 1
        spin = 0.1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.space_ship.body.ApplyLinearImpulse((0, 30), self.space_ship.body.position, True)

        if keys[pygame.K_w]:
            xxx = -math.sin(self.space_ship.body.angle)
            yyy = math.cos(self.space_ship.body.angle)
            self.space_ship.body.ApplyLinearImpulse((xxx * power, yyy * power), self.space_ship.body.worldCenter, True)

        if keys[pygame.K_d]:
            self.space_ship.body.ApplyAngularImpulse(-spin, True)

        if keys[pygame.K_a]:
            self.space_ship.body.ApplyAngularImpulse(spin, True)

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()

        # print(dir(self.space_ship.body))

        set_camera_position(self.space_ship.body.position[0], self.space_ship.body.position[1])
        # print(CAMERA_POSITION)


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(SpaceScene())
