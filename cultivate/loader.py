import os
from functools import lru_cache

import pygame
import pyganim
import random

from cultivate import settings

# todo: the spritesheets may be loaded from disk multiple tiles


@lru_cache(None)
def get_music(path: str) -> pygame.mixer.Sound:
    path = path.replace("/", os.sep).replace("\\", os.sep)
    path = os.path.join(settings.MUSIC_DIR, path)
    return pygame.mixer.Sound(path)


@lru_cache(None)
def get_sound(path: str) -> pygame.mixer.Sound:
    path = path.replace("/", os.sep).replace("\\", os.sep)
    path = os.path.join(settings.SOUNDS_DIR, path)
    return pygame.mixer.Sound(path)


@lru_cache(None)
def get_image(path: str, has_alpha: bool = False) -> pygame.Surface:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(canonicalized_path)
    if has_alpha:
        image.convert_alpha()
    else:
        image.convert()
    return image


@lru_cache(None)
def get_grass(width: int, height: int) -> pygame.Surface:
    # load the grass tile from the sprite sheet
    grass_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage4.png'),
        rects=[(269, 333, 16, 16)])[0].convert()

    # create a blank surface to paint with grass
    grass = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert()

    # paint grass tiles onto surface
    for i in range(0, height, 16):
        for j in range(0, width, 16):
            grass.blit(grass_tile, (i, j))
    return grass


@lru_cache(None)
def get_river(height):
    tiles = [
        (64, 48, 16, 16),  # left river
        (80, 48, 16, 16),  # middle river
        (112, 48, 16, 16)  # right river
    ]
    images = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'river1.png'),
        rects=tiles)
    for image in images:
        image.convert_alpha()
    river = pygame.Surface((48, height), pygame.SRCALPHA, 32).convert_alpha()

    # make left column
    for i in range(0, height, 16):
        river.blit(images[0], (0, i))
        river.blit(images[1], (16, i))
        river.blit(images[2], (32, i))
    return river


@lru_cache(None)
def get_floor(width: int, height: int) -> pygame.Surface:
    # load the floor tile from the sprite sheet
    floor_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'floors1.png'),
        rects=[(0, 0, 16, 16)])[0].convert()

    # create a blank surface to tile
    floor = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert()

    # tile the floor
    for i in range(0, height, 16):
        for j in range(0, width, 16):
            floor.blit(floor_tile, (i, j))
    return floor


@lru_cache(None)
def get_roof_small() -> pygame.Surface:
    return get_image(os.path.join(settings.SPRITES_DIR, "roof.png"), True)


@lru_cache(None)
def get_character(filename, direction):
    tiles = [
        (3, 130, 25, 36),  # facing forward
        (27, 130, 25, 36),
        (52, 130, 25, 36),
        (3, 166, 24, 34),  # facing backwards
        (27, 166, 26, 36),
        (52, 166, 26, 36),
        (3, 202, 25, 34),  # facing to the right
        (27, 202, 25, 34),
        (52, 202, 25, 34),
        (3, 236, 25, 34),  # facing to the right
        (27, 236, 25, 34),
        (52, 236, 25, 34)
    ]
    char_tiles = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, filename),
        rects=tiles)
    for tile in char_tiles:
        tile.convert_alpha()
    character = pygame.Surface(
        (23, 34), pygame.SRCALPHA, 32).convert_alpha()

    if direction == 'forward':
        dir_tiles = [
            char_tiles[0],
            char_tiles[1],
            char_tiles[0],
            char_tiles[2]
        ]
    elif direction == 'backward':
        dir_tiles = [
            char_tiles[3],
            char_tiles[4],
            char_tiles[3],
            char_tiles[5]
        ]
    elif direction == 'right':
        dir_tiles = [
            char_tiles[6],
            char_tiles[7],
            char_tiles[6],
            char_tiles[8]
        ]
    elif direction == 'left':
        dir_tiles = [
            char_tiles[9],
            char_tiles[10],
            char_tiles[9],
            char_tiles[11]
        ]
    else:
        dir_tiles = [
            char_tiles[0]
            ]
    frames = list(zip(dir_tiles,
                      [100, 100, 100, 100]))
    animChar = pyganim.PygAnimation(frames)
    animChar.play()

    return animChar

@lru_cache(None)
def get_player(direction=None):
    return get_character("chars1.png", direction)

@lru_cache(None)
def get_npc(direction=None):
    return get_character("chars1-2.png", direction)

@lru_cache(None)
def get_npc2(direction=None):
    tiles = [
        (1, 128, 30, 32), # forward
        (33, 128, 30, 32),
        (66, 128, 30, 32),
        (1, 160, 30, 32), # left
        (33, 160, 30, 32),
        (66, 160, 30, 32),
        (1, 192, 30, 32), # right
        (33, 192, 30, 32),
        (66, 192, 30, 32),
        (0, 224, 30, 32), # backward
        (33, 224, 30, 32),
        (66, 224, 30, 32)
    ]
    char_tiles = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "chars5.png"),
        rects=tiles)
    character = pygame.Surface(
        (30, 32), pygame.SRCALPHA, 32).convert_alpha()

    if direction == 'forward':
        dir_tiles = [
            char_tiles[0],
            char_tiles[1],
            char_tiles[0],
            char_tiles[2],
        ]
    elif direction == 'backward':
        dir_tiles = [
            char_tiles[9],
            char_tiles[10],
            char_tiles[9],
            char_tiles[11],
        ]
    elif direction == 'right':
        dir_tiles = [
            char_tiles[6],
            char_tiles[7],
            char_tiles[6],
            char_tiles[8],
        ]
    elif direction == 'left':
        dir_tiles = [
            char_tiles[3],
            char_tiles[4],
            char_tiles[3],
            char_tiles[5],
        ]
    else:
        dir_tiles = [
            char_tiles[0]
            ]
    frames = list(zip(dir_tiles,
                      [200, 200, 200, 200]))
    animChar = pyganim.PygAnimation(frames)
    animChar.play()
    return animChar

@lru_cache(None)
def get_npc_innocent(direction=None):
    tiles = [
        (1, 128, 30, 32), # forward
        (33, 128, 30, 32),
        (66, 128, 30, 32),
        (1, 160, 30, 32), # left
        (33, 160, 30, 32),
        (66, 160, 30, 32),
        (1, 192, 30, 32), # right
        (33, 192, 30, 32),
        (66, 192, 30, 32),
        (0, 224, 30, 32), # backward
        (33, 224, 30, 32),
        (66, 224, 30, 32)
    ]
    char_tiles = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "chars9.png"),
        rects=tiles)
    character = pygame.Surface(
        (30, 32), pygame.SRCALPHA, 32).convert_alpha()

    if direction == 'forward':
        dir_tiles = [
            char_tiles[0],
            char_tiles[1],
            char_tiles[0],
            char_tiles[2],
        ]
    elif direction == 'backward':
        dir_tiles = [
            char_tiles[9],
            char_tiles[10],
            char_tiles[9],
            char_tiles[11],
        ]
    elif direction == 'right':
        dir_tiles = [
            char_tiles[6],
            char_tiles[7],
            char_tiles[6],
            char_tiles[8],
        ]
    elif direction == 'left':
        dir_tiles = [
            char_tiles[3],
            char_tiles[4],
            char_tiles[3],
            char_tiles[5],
        ]
    else:
        dir_tiles = [
            char_tiles[0]
            ]
    frames = list(zip(dir_tiles,
                      [200, 200, 200, 200]))
    animChar = pyganim.PygAnimation(frames)
    animChar.play()
    return animChar

@lru_cache(None)
def get_npc3(direction=None):
    tiles = [
        (193, 128, 30, 32), # forward
        (225, 128, 30, 32),
        (257, 128, 30, 32),
        (193, 160, 30, 32), # left
        (225, 160, 30, 32),
        (257, 160, 30, 32),
        (193, 192, 30, 32), # right
        (225, 192, 30, 32),
        (257, 192, 30, 32),
        (193, 224, 30, 32), # backward
        (225, 224, 30, 32),
        (257, 224, 30, 32)
    ]
    char_tiles = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "chars5.png"),
        rects=tiles)
    character = pygame.Surface(
        (30, 32), pygame.SRCALPHA, 32).convert_alpha()

    if direction == 'forward':
        dir_tiles = [
            char_tiles[0],
            char_tiles[1],
            char_tiles[2]
        ]
    elif direction == 'backward':
        dir_tiles = [
            char_tiles[9],
            char_tiles[10],
            char_tiles[11]
        ]
    elif direction == 'right':
        dir_tiles = [
            char_tiles[6],
            char_tiles[7],
            char_tiles[8]
        ]
    elif direction == 'left':
        dir_tiles = [
            char_tiles[3],
            char_tiles[4],
            char_tiles[5]
        ]
    else:
        dir_tiles = [
            char_tiles[0]
            ]
    frames = list(zip(dir_tiles,
                      [100, 100, 100]))
    animChar = pyganim.PygAnimation(frames)
    animChar.play()
    return animChar

@lru_cache(None)
def get_npc4(direction=None):
    tiles = [
        (99, 2, 27, 31),
        (131, 2, 27, 31),
        (163, 2, 27, 31),
        (99, 34, 27, 31),
        (131, 34, 27, 31),
        (163, 34, 27, 31),
        (99, 66, 27, 31),
        (131, 66, 27, 31),
        (163, 66, 27, 31),
        (99, 98, 27, 31),
        (131, 98, 27, 31),
        (163, 98, 27, 31)
    ]
    char_tiles = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "chars6.png"),
        rects=tiles)
    character = pygame.Surface(
        (30, 32), pygame.SRCALPHA, 32).convert_alpha()

    if direction == 'forward':
        dir_tiles = [
            char_tiles[0],
            char_tiles[1],
            char_tiles[2]
        ]
    elif direction == 'backward':
        dir_tiles = [
            char_tiles[9],
            char_tiles[10],
            char_tiles[11]
        ]
    elif direction == 'right':
        dir_tiles = [
            char_tiles[6],
            char_tiles[7],
            char_tiles[8]
        ]
    elif direction == 'left':
        dir_tiles = [
            char_tiles[3],
            char_tiles[4],
            char_tiles[5]
        ]
    else:
        dir_tiles = [
            char_tiles[0]
            ]
    frames = list(zip(dir_tiles,
                      [100, 100, 100]))
    animChar = pyganim.PygAnimation(frames)
    animChar.play()
    return animChar

@lru_cache(None)
def get_laundry_basin():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'food1.png'),
        rects=[(160, 285, 34, 56)])[0].convert_alpha()

@lru_cache(None)
def get_lemonade_glass():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'food1.png'),
        rects=[(196, 258, 10, 14)])[0].convert_alpha()

@lru_cache(None)
def get_lemonade_pitcher():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'food1.png'),
        rects=[(227, 290, 18, 21)])[0].convert_alpha()

@lru_cache(None)
def get_rat_poison():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'food1.png'),
        rects=[(228, 259, 21, 18)])[0].convert_alpha()

@lru_cache(None)
def get_lemonade_stand():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'food1.png'),
        rects=[(192, 161, 65, 86)])[0].convert_alpha()

@lru_cache(None)
def get_bridge():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage1.png'),
        rects=[(416, 32, 95, 32)])[0].convert_alpha()

@lru_cache(None)
def get_laundry_basin_empty():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage1.png'),
        rects=[(159, 157, 33, 38)])[0].convert_alpha()

@lru_cache(None)
def get_dirt_path():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage4.png'),
        rects=[(130, 0, 28, 32)])[0].convert_alpha()


@lru_cache(None)
def get_weed():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "foliage2.png"),
        rects=[(131, 453, 58, 58)])[0].convert_alpha()


@lru_cache(None)
def get_walls(width):
    wall_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'walls2.png'),
        rects=[(65, 0, 62, 62)])[0].convert()
    wall = pygame.Surface((width, 62), pygame.SRCALPHA, 32).convert()
    for i in range(0, width, 62):
        wall.blit(wall_tile, (i, 0))
    return wall


@lru_cache(None)
def get_forest(width, height):
    tiles = [
        (0, 220, 130, 130),
        # this is the annoyingly long one in case you were wondering
        (258, 290, 125, 220),
        (130, 95, 120, 126),
        (133, 226, 120, 126)
    ]
    forest_tile = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, 'foliage2.png'),
        rects=tiles)
    for tile in forest_tile:
        tile.convert_alpha()
    forest = pygame.Surface(
        (width, height), pygame.SRCALPHA, 32).convert_alpha()

    # for top edge
    for i in range(0, width, 100):
        forest.blit(forest_tile[1], (i, -50))
        forest.blit(random.choice(forest_tile),
                    (i+random.randint(-30, 0), 0+random.randint(-20, 20)))
        forest.blit(random.choice(forest_tile),
                    (i+random.randint(-30, 0), 150+random.randint(-20, 20)))
        forest.blit(random.choice([forest_tile[0], forest_tile[2], forest_tile[3]]), (
            i+random.randint(-25, 25), 250+random.randint(-25, 25)))
    # left edge
    for i in range(0, height, 100):
        forest.blit(forest_tile[1], (-50, i+random.randint(-30, 0)))
        for i_x in range(50, 450, 90):
            forest.blit(random.choice(forest_tile),
                        (i_x+random.randint(-30, 30), i+random.randint(-30, 0)))
    # right edge
    for i in range(0, height, 100):
        forest.blit(forest_tile[1], (width-100, i+random.randint(-30, 0)))
        for i_x in range(50, 550, 90):
            forest.blit(random.choice(forest_tile), ((width - i_x) +
                                                     random.randint(-30, 30), i+random.randint(-30, 0)))
    # bottom edge
    for i in range(0, width, 100):
        for i_y in range(50, 400, 90):
            forest.blit(random.choice(
                forest_tile), (i+random.randint(-30, 0), (width - i_y)+random.randint(-30, 30)))
        forest.blit(forest_tile[1], (i, height-100))
    return forest


@lru_cache(None)
def get_lemon():
    return pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "food1.png"),
        rects=[(55, 180, 8, 8)])[0].convert_alpha()


@lru_cache(None)
def get_vegetables(width, height):
    tiles = [
        (10, 99, 41, 30),
        (10, 130, 41, 31),
        (10, 163, 41, 30),
        (10, 193, 41, 30),
        (10, 223, 41, 35),
        (10, 256, 41, 30)
    ]
    veg_tiles = pyganim.getImagesFromSpriteSheet(
        os.path.join(settings.SPRITES_DIR, "food1.png"),
        rects=tiles)
    for tile in veg_tiles:
        tile.convert_alpha()
    vegetables = pygame.Surface(
        (width, height), pygame.SRCALPHA, 32).convert_alpha()
    for i in range(50, width-30, 30):
        vegetables.blit(random.choice(veg_tiles), (0, i))
        vegetables.blit(random.choice(veg_tiles), (width-40, i))
    return vegetables
