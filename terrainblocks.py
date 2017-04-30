# Make terrain blocks

from constants import *
import pygame

BLOCK_DEFS = [
#    Asset         , RGBA Tint , Density, Friction, Restitution
    None,                                             # Air
    ['rock.png',     0x808080ff, 1.0,     0.2,      0.1], # 1  Rock
    ['granular.png', 0x803000ff, 1.0,     0.4,      0.4], # 2  Dirt
    ['leaves.png',   0x8000c0ff, 1.0,     0.3,      0.6], # 3  Purple leaves
    ['moss.png',     0x00c0ffff, 1.0,     0.3,      1.1], # 4  Blue fungus
    ['smooth.png',   0xc0c0ffff, 1.0,    0.01,      0.1], # 5  Ice
    ['flat.png',     0x00ff00ff, 1.0,     0.1,      0.1], # 6  Flat green tile
    ['granular.png', 0xc0c0c0ff, 1.0,     0.3,      0.2], # 7  Cobble
    ['smooth.png',   0xc0c0c0ff, 1.0,     0.4,      0.0], # 8  Dust
    ['leaves.png',   0x80ff00ff, 1.0,     0.3,      0.4], # 9  Grass
    ['rock.png',     0xc00000ff, 1.0,     0.2,      0.3], # 10 Mars
    ['granular.png', 0xff8000ff, 1.0,     0.4,      0.1], # 11 Orange Sand
    ['granular.png', 0xffe030ff, 1.0,     0.3,      0.2], # 12 Sand
    ['rock.png',     0xff8000ff, 1.0,     0.2,      0.3], # 13 Orange Rock
    ['moss.png',     0xff30c0ff, 1.0,     0.3,      1.1], # 14 Pink sponge
    ['granular.png', 0xc0d0ffff, 1.0,     0.2,      0.1], # 15 Permafrost
    ['smooth.png',   0xffffffff, 1.0,     0.5,      0.0], # 16 Snow
    ['smooth.png',   0xc0d0ffff, 1.0,     0.1,      0.2], # 17 Metal
    ['leaves.png',   0xffc0d0ff, 1.0,     0.1,      0.2], # 18 Crystal
    ['smooth.png',   0xffc0807f, 1.0,     0.5,      0.0], # 19 Fog
]

BLOCK_IMAGES = []
WALL_IMAGES = []

def make_blocks(block_scale):
    block_mask = pygame.image.load(os.path.join(ASSETS_PATH, 'blockmask.png')).convert_alpha()
    ratio = block_mask.get_height() / block_mask.get_width()
    w = int(1.6 * block_scale * SHAPE_UNITS_TO_METRES)
    h = int(1.6 * block_scale * SHAPE_UNITS_TO_METRES * ratio)

    for b in BLOCK_DEFS:
        if not b:
            BLOCK_IMAGES.append(None)
            WALL_IMAGES.append(None)
            continue
        asset, tint, density, friction, restitution = b

        rgba = [ (tint>>offset) & 0xff for offset in [24, 16, 8, 0] ]

        image = pygame.image.load(os.path.join(ASSETS_PATH, asset)).convert_alpha()
        image.blit(block_mask, image.get_rect(), special_flags=pygame.BLEND_RGBA_MULT)
        image = pygame.transform.scale(image, (w, h))
        image.fill(rgba, special_flags=pygame.BLEND_RGBA_MULT)
        BLOCK_IMAGES.append(image)
        wimage = image.copy()
        wimage.fill((96,96,96,255), special_flags=pygame.BLEND_RGBA_MULT)
        WALL_IMAGES.append(wimage)
    print("Loaded %d block images" % len(BLOCK_IMAGES))
