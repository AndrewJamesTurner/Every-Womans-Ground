#!/usr/bin/env python3
import ezpygame
from Box2D import b2World, b2PolygonShape, b2ContactListener

import lander_shapes as landershapes
import shapes
from game import *
from terraingen import *
from GameScene import GameScene
import terrain_utils

from GameObject import *

change_to_space_scene = False

class LanderScene(GameScene):

    def __init__(self):
        super(LanderScene, self).__init__()
        self.savedLanderPos = None

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        global change_to_space_scene
        change_to_space_scene = False

        # self.planet_info = {
        #     "name": "Earth",
        #     "size": 10,
        #     "angular_vel": 0.0001,
        #     "orbit_radius_x": 30,
        #     "orbit_radius_y": 35,
        #     "orbit_angle": 0.13,
        #     "type": "ice",
        #     "orbit_centre": (0, 0),
        #     "seed": 53,
        #     "dist_to_asteroid_belt": 30
        # }

        self.planet_info = get_space_scene().planet_info
        params = terrain_utils.get_planet_params( self.planet_info["type"], self.planet_info)

        # Set countdown for landing
        self.countdown = None

        # Called once per game, when game starts

        self.world = b2World(contactListener=ContactListener())  # default gravity is (0,-10) and doSleep is True

        # Set gravity depending on planet type.
        self.world.gravity = (0, -params["gravity"])

        # Set camera to centre
        set_camera_position(0, (SCREEN_HEIGHT / PPM) / 2)

        # Match values to zoomed-in scale
        planet_lander_scale = 3.0
        numPoints = 32

        # There are 500 points in the planet view
        xGap = 500 / numPoints / planet_lander_scale
        height_multi = 1 / planet_lander_scale

        #print("-----------------")
        #print(terrain_utils.terrain_params[self.planet_info['type']]["ratio"])
        #print("-----------------")

        # Use the same randomizer as the on-planet gen to get the same terrain
        r = random.Random(self.planet_info['seed'])
        terrain_seed = r.getrandbits(32)
        r = random.Random(terrain_seed)
        seed_groundbase = r.getrandbits(32)

        tparams = terrain_utils.terrain_params[self.planet_info['type']]
        height = tparams['depth'] * height_multi
        terrain = generate_fractal_heightmap(seed_groundbase, numPoints, height, tparams['ratio'])

        # polygons can't have many edges so split into separate polygons
        bottom = -(SCREEN_HEIGHT / PPM)

        polygonArray = []

        for index, terrainVal in enumerate(terrain):
            x = (index - numPoints / 2) * xGap
            y = terrainVal
            if index > 0:
                polygonPoints=[ [x-xGap,bottom],[x-xGap, lasty],
                                [ x    , y ],[ x       , bottom ] ]
                polygonArray.append(polygonPoints)
            lasty = y

        # print(polygonArray)

        self.ground = landershapes.PlanetGround(self.world, (0, 0), polygonArray)
        if self.planet_info['type'] == "rock":
            self.ground.colour = (146, 149, 153, 0)
            friction    = 0.4
            restitution = 0.1
        elif self.planet_info['type'] == "earth":
            self.ground.colour = (43, 109, 49, 0)
            friction    = 0.4
            restitution = 0.4
        elif self.planet_info['type'] == "desert":
            self.ground.colour = (198, 87, 65, 0)
            friction    = 0.3
            restitution = 0.2
        elif self.planet_info['type'] == "gas":
            self.ground.colour = (105, 181, 188, 0)
            friction = 0.1
            restitution = 0.2
        elif self.planet_info['type'] == "ice":
            self.ground.colour = (142, 239, 249, 0)
            friction    = 0.01
            restitution = 0.1
        elif self.planet_info['type'] == "other":
            self.ground.colour = (224, 167, 130, 0)
            friction = 0.3
            restitution = 1.1
        else:
            self.ground.colour = (43, 109, 49, 0)
            friction    = 1.0
            restitution = 0.0

        self.ground.body.friction = friction
        self.ground.body.restitution = restitution

        # Add the lander in the middle of the ground
        landerStartHeight = max(terrain) + 2


        if previous_scene == get_planet_scene():
            self.lander = landershapes.Lander(self.world, self.savedLanderPos)
            self.countDownLen = 10000
        else:
            self.lander = landershapes.Lander(self.world,
                                          (0, landerStartHeight + (SCREEN_HEIGHT / PPM) / 2))
            self.countDownLen = 2000

        self.lander.body.angularDamping = 0.2


        self.ship = landershapes.StationarySpaceship(self.world, ( -(SCREEN_WIDTH / PPM) / 3, landerStartHeight + (3 * SCREEN_HEIGHT / PPM) / 4))

        self.skydrop = shapes.ParallaxBackdrop(5, os.path.join(ASSETS_PATH, 'backdrop3.jpg'), numPoints * xGap)


    def handle_event(self, event):
        # Called every time a pygame event is fired

        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Do something

        pass

    def draw(self, screen):
        # Called once per frame, to draw to the screen

        screen.fill(black)
        self.skydrop.draw(screen)
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

        power = 3.5

        landerPos = self.lander.body.position

        # Processing keyboard input here gives one event per key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.lander.body.angle += 0.02
            get_shared_values().fuel -= 0.25;
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.lander.body.angle -= 0.02
            get_shared_values().fuel -= 0.25;

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.lander.body.ApplyLinearImpulse((xxx * power, yyy * power), (landerPos[0]+0.005, landerPos[1]), True)
            get_shared_values().fuel -= 1;

        if keys[pygame.K_ESCAPE]:
            exit()

        set_camera_position(self.lander.body.position[0],self.lander.body.position[1])

        angleOfImpact = self.lander.body.angle
        angleOfImpact = abs(math.fmod(angleOfImpact, 2 * math.pi))

        if angleOfImpact > math.pi:
            angleOfImpact -= math.pi

        #Get velocity of lander
        if self.lander.body.linearVelocity == (0,0) and angleOfImpact < 0.5:
            if self.countdown == None:
                self.countdown = 0
            else:
                self.countdown += dt
        else:
            self.countdown = None

        if self.countdown != None:
            if self.countdown >= self.countDownLen:
                #print('landed')

                self.savedLanderPos = (self.lander.body.position[0], self.lander.body.position[1]+0.2)
                self.application.change_scene(get_planet_scene())

        self.check_game_over()



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
                    #print('angle small damage')
                if angleOfImpact > 1.5:
                    get_shared_values().health -= 5.0;
                    #print('angle big damage')
                if angleOfImpact > 2.0:
                    get_shared_values().health -= 10.0;
                    #print('angle huge damage')

                #Check for extreme velocity
                fixtureAVelocity = contact.fixtureA.body.GetLinearVelocityFromWorldPoint(contact.worldManifold.points[0])
                fixtureBVelocity = contact.fixtureB.body.GetLinearVelocityFromWorldPoint(contact.worldManifold.points[0])

                velocity = (fixtureAVelocity-fixtureBVelocity).length
                if velocity >= 5:
                    get_shared_values().health -= 2.0;
                    #print('hit small damage')
                if velocity >= 10:
                    get_shared_values().health -= 5.0;
                    #print('hit big damage')

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_lander_scene())
