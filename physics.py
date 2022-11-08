import pygame
import math
import numpy as np

import assets
import settings
from world import WorldEngine


class Physics:
    def __init__(self, worldengine_ref:WorldEngine) -> None:
        self.world_engine = worldengine_ref
        self.entities: Entity = []
        self.entities.append(Entity(self.world_engine, (80,64), (16,16), assets.textureMap["test_entity"]))
        self.entities.append(Entity(self.world_engine, (40,40), (16,16), assets.textureMap["test_entity"]))
        self.player = Player(self.world_engine, (40,40), (32,64), assets.textureMap["player_entity"])

    def tick(self):
        self.player.move((self.player.speed_x, self.player.speed_y))
        for entity in self.entities:
            entity.move((0.1, 0))
        
        

class Entity(pygame.sprite.Sprite):
    def __init__(self, wordlengine_ref:WorldEngine, pos:tuple, size:tuple, image:pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.world_engine = wordlengine_ref
        self.__pos = list(pos)
        self.size = size
        self.image = image    
        self.update_rect
             
        
    def update_rect(self):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.__pos[0], self.__pos[1])
    
    def move(self, movement:tuple, *, recursion_depth:int=0):
        self.__pos[0] += movement[0]
        self.__pos[1] += movement[1]
        self.update_rect()
        if pygame.sprite.spritecollideany(self, self.world_engine.block_sprite_group) and recursion_depth <10:
            self.__pos[0] -= movement[0]
            self.__pos[1] -= movement[1]
            self.move((movement[0]-np.sign(movement[0]), movement[1]-np.sign(movement[1])), recursion_depth=recursion_depth+1)
            
    def get_pos(self) -> tuple:
        return self.__pos
            

class Player(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, pos: tuple, size: tuple, image: pygame.image) -> None:
        super().__init__(wordlengine_ref, pos, size, image)
        self.speed_x = 0
        self.speed_y = 0

    
class Enemies(Entity):
     def __init__(self) -> None:
        pass
    