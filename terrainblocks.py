# Make terrain blocks

from constants import *
import pygame

BLOCK_DEFS = [
#    Asset         , RGBA Tint , Density, Friction, Restitution
    None,                                             # Air
    ['rock.png',     0x808080ff, 1.0,     0.3,      0.4], # Rock
    ['granular.png', 0x803000ff, 1.0,     0.3,      0.4], # Dirt
    ['leaves.png',   0x300080ff, 1.0,     0.3,      0.4], # Purple leaves
    ['moss.png',     0x00c0ffff, 1.0,     0.3,      0.4], # Blue fungus
    ['smooth.png',   0xc0c0ffff, 1.0,     0.3,      0.4], # Ice
    ['flat.png',     0x00ff00ff, 1.0,     0.3,      0.4], # Flat green tile
]

BLOCK_IMAGES = []

def make_blocks(block_scale):
    for b in BLOCK_DEFS:
        if not b:
            BLOCK_IMAGES.append(None)
            continue
        asset, tint, density, friction, restitution = b

        rgba = [ (tint>>offset) & 0xff for offset in [24, 16, 8, 0] ]

        image = pygame.image.load(os.path.join(ASSETS_PATH, asset)).convert_alpha()
        ratio = image.get_height() / image.get_width()
        w = int(block_scale * SHAPE_UNITS_TO_METRES)
        h = int(block_scale * SHAPE_UNITS_TO_METRES * ratio)
        image = pygame.transform.scale(image, (w, h))
        image.fill(rgba, special_flags=pygame.BLEND_RGBA_MULT)
        BLOCK_IMAGES.append(image)
    print("Loaded %d block images" % len(BLOCK_IMAGES))
