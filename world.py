from dataclasses import dataclass
import pygame
import numpy as np
import settings

@dataclass
class Wall:
    x1: int
    y1: int
    x2: int
    y2: int

    def draw(self, screen, ofsett:tuple):
        pygame.draw.line(screen, (255,255,255), (self.x1+ofsett[0], self.y1+ofsett[1]), (self.x2+ofsett[0], self.y2+ofsett[1]))

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
        
        self.update_world_walls()
        self.update_block_list()

    def save_world_to_memory(self):
        np.save(f"{settings.dictPath}/worlds/{self.world_name}.npy", self.world)       

    def get_block(self, block_position:tuple[int, int]) -> int:
        return self.world[block_position[0]][block_position[1]]

    def set_block(self, block_position:tuple[int, int], block_value: int) -> None:
        self.world[block_position[0]][block_position[1]] = block_value
        self.update_block_list()
        
    def get_walls_for_block(self, block_pos:tuple) -> tuple:
        top = Wall((block_pos[0])*self.blocksize, (block_pos[1])*self.blocksize, (block_pos[0]+1)*self.blocksize, (block_pos[1])*self.blocksize)
        
        right = Wall((block_pos[0]+1)*self.blocksize,
            (block_pos[1])*self.blocksize,
            (block_pos[0]+1)*self.blocksize,
            (block_pos[1]+1)*self.blocksize)
        
        bottom = Wall((block_pos[0])*self.blocksize,
            (block_pos[1]+1)*self.blocksize,
            (block_pos[0]+1)*self.blocksize,
            (block_pos[1]+1)*self.blocksize)
        
        left = Wall((block_pos[0])*self.blocksize,
            (block_pos[1])*self.blocksize,
            (block_pos[0])*self.blocksize,
            (block_pos[1]+1)*self.blocksize)
        
        return top, right, bottom, left
        
    def update_world_walls(self) -> None:
        self.walls = []
        for lineIndex, line in enumerate(self.world):
            for blockIndex, block in enumerate(line):
                if block in self.collision_list:
                    self.walls += self.get_walls_for_block((lineIndex, blockIndex))
                    print("added walls!")
                
    def update_block_list(self):
        self.block_list = []
        for xIndex, xList in enumerate(self.world):
            for yIndex, block in enumerate(xList):
                if block != 0 :
                    self.block_list.append(((xIndex, yIndex), block))


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