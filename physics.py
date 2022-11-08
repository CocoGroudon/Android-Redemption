import pygame
import math

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
        
        

class Entity:
    def __init__(self, wordlengine_ref:WorldEngine, pos:tuple, size:tuple, image:pygame.image) -> None:
        self.world_engine = wordlengine_ref
        self.pos = list(pos)
        self.size = size
        self.image = image         
    
    def move(self, movement:tuple):
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
            

class Player(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, pos: tuple, size: tuple, image: pygame.image) -> None:
        super().__init__(wordlengine_ref, pos, size, image)
        self.speed_x = 0
        self.speed_y = 0

    
class Enemies(Entity):
     def __init__(self) -> None:
        pass
    