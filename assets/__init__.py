import pygame
from pathlib import Path

textureMap = {
    "windowicon" : pygame.image.load(Path(__file__).with_name('windowicon.png')),
    "player": pygame.image.load(Path(__file__).with_name('Mänchen.png')),
    0 : pygame.image.load(Path(__file__).with_name('white.png')),
    1 : pygame.image.load(Path(__file__).with_name('blue.png')),
    2 : pygame.image.load(Path(__file__).with_name('bedrock.png')),
    3 : pygame.image.load(Path(__file__).with_name('turquise.png')),
    4 : pygame.image.load(Path(__file__).with_name('red.png'))

}