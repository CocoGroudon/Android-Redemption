import os 
from pathlib import Path
import pygame

framerate = 0
backgroundcolor = (0, 43, 53)
blocksize = 32

# World
world_name = "test"
world_dimensions = (500, 100)

# Physics
entity_move_rays_ofsett = 0.01

# Renderer
block_choices_screen_ofsett = (0,200)
block_choices = (0,1,2,127)
render_walls = False

keybinds = {
    "up": pygame.K_w,
    "left": pygame.K_a,
    "down": pygame.K_s,
    "right": pygame.K_d,
    "toggle_fullscreen": pygame.K_F11
}

dictPath = os.path.dirname(Path(__file__))