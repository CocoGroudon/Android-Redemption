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
projectile_speed = 1000
projectile_lifetime = 10

player_jump_strength = 200
gravity = True
grav_strenght = 200

# Player
inventory_size = (5,9)
inventory_item_size = 8 # Pixel

item_size = (16, 16)

# Renderer
block_choices_screen_ofsett = (0,200)
block_choices = (0,1,2,3,127)

keybinds = {
    "up": [pygame.K_SPACE, pygame.K_UP ],
    "left": [pygame.K_a, pygame.K_LEFT ],
    "down": [pygame.K_s, pygame.K_DOWN ],
    "right": [pygame.K_d, pygame.K_RIGHT ],
    "toggle_fullscreen": pygame.K_F11,
    "action": [pygame.K_1]
}

dictPath = os.path.dirname(Path(__file__))