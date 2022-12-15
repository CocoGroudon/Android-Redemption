import pygame
from pathlib import Path
import sys
import os
import settings



pygame.display.init()
screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        filename = os.path.basename(filename)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


def load_image(path:str) -> pygame.image:
    new_path = find_data_file(path)
    image = pygame.image.load(new_path)
    return image
    
    
textureMap = {
    "test_entity": load_image('test_entity.png').convert_alpha(),
    "player_entity": load_image('playerasset.png').convert_alpha(),
    "test_projectile": load_image('test_projectile.png').convert_alpha(),
    "heart": load_image('heart.png').convert_alpha(),
    0 : load_image('luft.png').convert_alpha(),
    1 : load_image('stein.png').convert_alpha(),
    2 : load_image('grass.png').convert_alpha(),
    3 : load_image('lava.png').convert_alpha(),
    127 : load_image('testtexture.png').convert_alpha()
}

paralax_background = {
    0 : pygame.transform.scale2x(load_image('background/sky.png')).convert_alpha(),
    1 : pygame.transform.scale2x(load_image('background/far-clouds.png')).convert_alpha(),
    2 : pygame.transform.scale2x(load_image('background/near-clouds.png')).convert_alpha(),
    3 : pygame.transform.scale2x(load_image('background/far-mountains.png')).convert_alpha(),
    4 : pygame.transform.scale2x(load_image('background/mountains.png')).convert_alpha(),
    5 : pygame.transform.scale2x(load_image('background/trees.png')).convert_alpha()
}

texture_item = {
    "weed": load_image("weed.png").convert_alpha(),
    'Flamethrower': pygame.transform.scale(load_image('items/item_flamethrower.png'), (16,16)).convert_alpha(),
    1 : load_image('item_dirt.png').convert_alpha()
}

projectiles = {
    "bullet": load_image('projectiles/bullet.png').convert_alpha(),
    "flame": load_image('projectiles/firesll_32x17.png').convert_alpha()
}