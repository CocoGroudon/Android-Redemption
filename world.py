from dataclasses import dataclass
import pygame
import numpy as np
import settings
import assets


class WorldEngine:
    def __init__(self) -> None:
        self.world_name = settings.world_name
        
        self.walls = []
        self.block_list = []
        self.collision_list = (1,2,3,4,5,6, 127)
        self.blocksize = settings.blocksize
        
        # self.load_world_from_memory()

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


class Block_Sprite(pygame.sprite.Sprite):
    def __init__(self, value:int, pos:tuple) -> None:
        pygame.sprite.Sprite.__init__(self=self)
        # self.width = settings.blocksize
        # self.height = settings.blocksize
        
        
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