#!/usr/bin/env python3
import ezpygame
from Box2D import b2World, b2PolygonShape, b2ContactListener

import lander_shapes as landershapes
from game import *
from terraingen import *
from GameScene import GameScene

from GameObject import *

change_to_space_scene = False

class LanderScene(GameScene):

    def __init__(self):
        super(LanderScene, self).__init__()


    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        global change_to_space_scene
        change_to_space_scene = False

        self.planet_info = {
            "name": "Earth",
            "size": 10,
            "angular_vel": 0.0001,
            "orbit_radius_x": 30,
            "orbit_radius_y": 35,
            "orbit_angle": 0.13,
            "type": "other",
            "orbit_centre": (0, 0),
            "seed": 6
        }

        # Set countdown for landing
        self.countdown = None

        # Called once per game, when game starts

        self.world = b2World(contactListener=ContactListener())  # default gravity is (0,-10) and doSleep is True

        # Set gravity depending on planet type.
        self.world.gravity = (0, -5)

        # Set camera to centre
        set_camera_position((SCREEN_WIDTH / PPM) / 2, (SCREEN_HEIGHT / PPM) / 2)

        # Need to generate a seed
        # Need to set height and xgap based on planet info
        numPoints = 100

        terrain = generate_fractal_heightmap(self.planet_info['seed'] + 117, numPoints, int(SCREEN_HEIGHT / PPM) / 4, 1)

        # polygons can't have many edges so split into separate polygons
        starty = -100
        pointCountDown = 10
        startCoords = [0, starty]
        xGap = 5

        polygonArray = []
        polygonPoints = [startCoords]

        for index, terrainVal in enumerate(terrain):

            polygonPoints.append([index * xGap, terrainVal])

            if pointCountDown > 0:
                pointCountDown -= 1
            else:
                # finish block and reset counter
                polygonPoints.append([index * xGap, starty])
                polygonArray.append(polygonPoints)

                # Use 9 here because we initialise with two values
                pointCountDown = 9
                polygonPoints = [[index * xGap, starty], [index * xGap, terrainVal]]

        print(polygonArray)

        self.ground = landershapes.PlanetGround(self.world, (0, 0), polygonArray)
        if self.planet_info['type'] == "rock":
            self.ground.colour = (146, 149, 153, 0)
        elif self.planet_info['type'] == "earth":
            self.ground.colour = (43, 109, 49, 0)
        elif self.planet_info['type'] == "desert":
            self.ground.colour = (198, 87, 65, 0)
        elif self.planet_info['type'] == "gas":
            self.ground.colour = (105, 181, 188, 0)
        elif self.planet_info['type'] == "ice":
            self.ground.colour = (142, 239, 249, 0)
        elif self.planet_info['type'] == "other":
            self.ground.colour = (224, 167, 130, 0)
        else:
            self.ground.colour = (43, 109, 49, 0)
        # Add the lander in the middle of the ground
        landerStartHeight = 5
        self.lander = landershapes.Lander(self.world,
                                          ((xGap * numPoints) / 2, landerStartHeight + (SCREEN_HEIGHT / PPM) / 2))
        self.ship = landershapes.StationarySpaceship(self.world, (
        (xGap * numPoints) / 2 - (SCREEN_WIDTH / PPM) / 3, landerStartHeight + (3 * SCREEN_HEIGHT / PPM) / 4))

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
        self.ship.draw(screen)
        self.lander.draw(screen)


        #If using sensors use this
        # shape = self.lander.sensor.shape
        # vertices = [world_to_screen_coordinates(self.lander.body.transform * v) for v in shape.vertices]
        # pygame.draw.polygon(screen, (255,255,255,0), vertices)

        self.draw_overlays(screen)

    def update(self, dt):
        # Called once per frame, to update the state of the game

        # Processing keyboard events here lets you track which keys are being held down
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.lander.body.ApplyLinearImpulse((0, 30), self.lander.body.position, True)

        # Box2d physics step
        self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        self.world.ClearForces()

        global change_to_space_scene
        if change_to_space_scene:
            self.application.change_scene(get_space_scene())

        xxx = -math.sin(self.lander.body.angle)
        yyy = math.cos(self.lander.body.angle)

        power = 1

        landerPos = self.lander.body.position

        # Processing keyboard input here gives one event per key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.lander.body.angle += 0.01
            get_shared_values().fuel -= 0.25;
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.lander.body.angle -= 0.01
            get_shared_values().fuel -= 0.25;

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.lander.body.ApplyLinearImpulse((xxx * power, yyy * power), landerPos, True)
            get_shared_values().fuel -= 1;

        set_camera_position(self.lander.body.position[0],self.lander.body.position[1])

        angleOfImpact = self.lander.body.angle
        angleOfImpact = abs(math.fmod(angleOfImpact, 2 * math.pi))

        if angleOfImpact > math.pi:
            angleOfImpact -= math.pi

        countDownLen = 3000
        #Get velocity of lander
        if self.lander.body.linearVelocity == (0,0) and angleOfImpact < 0.5:
            if self.countdown == None:
                self.countdown = 0
            else:
                self.countdown += dt
        else:
            self.countdown = None

        if self.countdown != None:
            if self.countdown >= countDownLen:
                print('landed')

                self.application.change_scene(get_planet_scene())


class ContactListener(b2ContactListener):

    def BeginContact(self, contact):

        #If using sensor use this
        # if contact.fixtureA.userData == "LanderCollisionArea" or contact.fixtureB.userData == "LanderCollisionArea":
        #     print('ouch! Damage - lose some health')
        if isinstance(contact.fixtureA.body.userData, landershapes.Lander) or isinstance(contact.fixtureB.body.userData, landershapes.Lander):

            if isinstance(contact.fixtureA.body.userData, landershapes.StationarySpaceship) or isinstance(contact.fixtureB.body.userData, landershapes.StationarySpaceship):

                #get_lander_scene().application.change_scene(get_space_scene())
                global change_to_space_scene
                change_to_space_scene = True

            else:
                #Check for silly angle
                if isinstance(contact.fixtureA.body.userData, landershapes.Lander):
                    angleOfImpact = contact.fixtureA.body.userData.body.angle
                elif isinstance(contact.fixtureB.body.userData, landershapes.Lander):
                    angleOfImpact = contact.fixtureB.body.userData.body.angle

                angleOfImpact = abs(math.fmod(angleOfImpact, 2 * math.pi))

                if angleOfImpact > math.pi:
                    angleOfImpact -= math.pi

                if angleOfImpact > 0.5:
                    get_shared_values().health -= 2.0;
                    print('angle small damage')
                if angleOfImpact > 1.5:
                    get_shared_values().health -= 5.0;
                    print('angle big damage')
                if angleOfImpact > 2.0:
                    get_shared_values().health -= 10.0;
                    print('angle huge damage')

                #Check for extreme velocity
                fixtureAVelocity = contact.fixtureA.body.GetLinearVelocityFromWorldPoint(contact.worldManifold.points[0])
                fixtureBVelocity = contact.fixtureB.body.GetLinearVelocityFromWorldPoint(contact.worldManifold.points[0])

                velocity = (fixtureAVelocity-fixtureBVelocity).length
                if velocity >= 5:
                    get_shared_values().health -= 2.0;
                    print('hit small damage')
                if velocity >= 10:
                    get_shared_values().health -= 5.0;
                    print('hit big damage')

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_lander_scene())
