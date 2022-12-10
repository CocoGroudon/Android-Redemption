from dataclasses import dataclass
import pygame
import numpy as np
import random
import sys
import os

import settings
import assets

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
class WorldEngine:
    def __init__(self) -> None:
        self.world_name = settings.world_name
        self.world = np.zeros((1,1))
        self.refresh_block_group()
        
        self.block_list = []
        # self.collision_list = (1,2,3,4,5,6, 127)
        
        
    def set_new_world(self, dimensions:tuple[int, int]) -> None:
        self.world = np.zeros((dimensions[0], dimensions[1]), dtype=np.int8)

    def load_world_from_memory(self) -> None:
        self.world = np.load(f"{settings.dictPath}/worlds/{self.world_name}.npy")
        
        self.refresh_block_group()

    def save_world_to_memory(self):
        np.save(f"{settings.dictPath}/worlds/{self.world_name}.npy", self.world)       

    def get_block(self, block_position:tuple[int, int]) -> int:
        return self.world[block_position[0]][block_position[1]]

    def set_block(self, block_position:tuple[int, int], block_value: int) -> None:
        print(block_position)
        try:
            self.world[block_position[0]][block_position[1]] = block_value
            self.update_block_list()
        except IndexError:
            print("Player placed block out of bounds!")
                
    def refresh_block_group(self):
        self.block_sprite_group = pygame.sprite.Group()
        block_sprites = []
        self.update_block_list()
        for block_pos, value in self.block_list:
            sprite = Block_Sprite(value, block_pos)
            block_sprites.append(sprite)
        self.block_sprite_group.add(block_sprites)
        
    def update_block_list(self):
        self.block_list = []
        for xIndex, xList in enumerate(self.world):
            for yIndex, block in enumerate(xList):
                if block != 0 :
                    self.block_list.append(((xIndex, yIndex), block))
                    
    def _get_room(self, room_name:str) -> np.array:
        myPath = find_data_file(f"/worlds/{room_name}.npy")
        return np.load(myPath)
                    
    def create_new_random_world(self, amount_of_rooms: int):
        room_name_list = [random.choice(settings.world_room_options) for _ in range(amount_of_rooms)]
        room_array_list = [self._get_room(name) for name in room_name_list]
        room_width_list = [len(room) for room in room_array_list]
        room_height_list = [len(room[0]) for room in room_array_list]
        
        height = max(room_height_list)
        width = sum(room_width_list)
        
        world = np.zeros((width, height), dtype=np.int8)
        world_current_fill_pos = 0
        for room_index, room in enumerate(room_array_list):
            for line_index, line in enumerate(room):
                for col_index, cell in enumerate(line):
                    world[line_index+world_current_fill_pos][col_index] = cell
            world_current_fill_pos += room_width_list[room_index]
        return world
        


class Block_Sprite(pygame.sprite.Sprite):
    def __init__(self, value:int, pos:tuple) -> None:
        pygame.sprite.Sprite.__init__(self=self)
      
        self.image = assets.textureMap[value]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos[0]*settings.blocksize, pos[1]*settings.blocksize)

if __name__ == "__main__":
    world_engine = WorldEngine()    
    world_engine.set_new_world(settings.world_dimensions)
    world_engine.set_block((5,2), 127)
    world_engine.set_block((1,2), 1)
    world_engine.set_block((2,2), 1)
    world_engine.set_block((3,2), 1)
    world_engine.set_block((6,0), 1)
    world_engine.set_block((6,1), 1)
    world_engine.set_block((6,2), 1)
    world_engine.save_world_to_memory()