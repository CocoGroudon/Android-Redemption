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
    "test_entity": load_image('test_entity.png'),
    "player_entity": load_image('playerasset.png'),
    "test_projectile": load_image('test_projectile.png'),
    "heart": load_image('heart.png'),
    "projectile": load_image('projectile.png'),
    0 : load_image('luft.png'),
    1 : load_image('stein.png'),
    2 : load_image('grass.png'),
    3 : load_image('lava.png'),
    127 : load_image('testtexture.png')
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
    "weed": load_image("weed.png"),
    'Flamethrower': pygame.transform.scale(load_image('items/item_flamethrower.png'), (16,16)),
    1 : pygame.image.load(Path(__file__).with_name('item_dirt.png')),
}