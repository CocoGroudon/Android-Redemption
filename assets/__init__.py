import pygame
from pathlib import Path

textureMap = {
    "test_entity": pygame.image.load(Path(__file__).with_name('test_entity.png')),
    "player_entity": pygame.image.load(Path(__file__).with_name('playerasset.png')),
    "test_projectile": pygame.image.load(Path(__file__).with_name('test_projectile.png')),
    "heart": pygame.image.load(Path(__file__).with_name('heart.png')),
    0 : pygame.image.load(Path(__file__).with_name('luft.png')),
    1 : pygame.image.load(Path(__file__).with_name('stein.png')),
    2 : pygame.image.load(Path(__file__).with_name('grass.png')),
    3 : pygame.image.load(Path(__file__).with_name('lava.png')),
    127 : pygame.image.load(Path(__file__).with_name('testtexture.png'))
}


texture_item = {
    1 : pygame.image.load(Path(__file__).with_name('item_dirt.png')),
}