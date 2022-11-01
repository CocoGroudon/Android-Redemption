import pygame
from pathlib import Path

textureMap = {
    0 : pygame.image.load(Path(__file__).with_name('luft.png')),
    1 : pygame.image.load(Path(__file__).with_name('stein.png')),
    2 : pygame.image.load(Path(__file__).with_name('grass.png'))
}