import os

# Window size, in pixels
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Pixels per meter, converting between box2d world and pygame screen
PPM = 20.0

# Frames per second, for rendering and physics
FPS = 60

# Conversion between ezpygame dt and box2d dt
DT_SCALE = 0.001

# Box2d iteration parameters
VELOCITY_ITERATIONS = 10
POSITION_ITERATIONS = 10

# Number of box2d metres for every unit in our shape definition units
SHAPE_UNITS_TO_METRES = 20

# Pygame colour
black = 0, 0, 0, 0
white = 255, 255, 255, 0
red = 255, 0, 0, 0
yellow = 255, 255, 0, 0

ASSETS_PATH = 'assets'
BIOMES = ['desert', 'water', 'ice', 'lava', 'forest']

# TODO Fill in other textures
BIOME_TEXTURES = {0: os.path.join(ASSETS_PATH, 'terrain_block_blue.png'),
                  1: os.path.join(ASSETS_PATH, 'terrain_block_blue.png'),
                  2: os.path.join(ASSETS_PATH, 'terrain_block_blue.png'),
                  3: os.path.join(ASSETS_PATH, 'terrain_block_blue.png'),
                  4: os.path.join(ASSETS_PATH, 'terrain_block_blue.png'),
                  }