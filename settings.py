import os 
from pathlib import Path
import pygame

framerate = 0
backgroundcolor = (0, 43, 53)

world_name = "test"
world_dimensions = (500, 100)

keybinds = {
    "up": pygame.K_w,
    "left": pygame.K_a,
    "down": pygame.K_s,
    "right": pygame.K_d,
    "toggle_fullscreen": pygame.K_F11
}

blocksize = 32
dictPath = os.path.dirname(Path(__file__))