import pygame
from pathlib import Path

textureMap = {
    "test_entity": pygame.image.load(Path(__file__).with_name('test_entity.png')),
    0 : pygame.image.load(Path(__file__).with_name('luft.png')),
    1 : pygame.image.load(Path(__file__).with_name('stein.png')),
    2 : pygame.image.load(Path(__file__).with_name('grass.png')),
    127 : pygame.image.load(Path(__file__).with_name('testtexture.png'))
}