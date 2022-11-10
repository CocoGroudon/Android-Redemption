import pygame
import math
import numpy as np
import time 

import assets
import settings
from world import WorldEngine

class Physics:
    def __init__(self, worldengine_ref:WorldEngine, game_ref) -> None:
        self.world_engine = worldengine_ref
        self.game = game_ref
        
        self.entities: Entity = []
        self.entities.append(Entity(self.world_engine, (80,64), (16,16), assets.textureMap["test_entity"]))
        self.entities.append(Entity(self.world_engine, (40,40), (16,16), assets.textureMap["test_entity"]))
        self.player = Player(self.world_engine, (40,40), (32,64), assets.textureMap["player_entity"])

    def tick(self):
        # Setup for Tick
        fps = self.game.clock.get_fps()
        if fps == 0: return
        tick_lenght = 1/fps


        if settings.gravity:
            self.player.speed_y -= settings.grav_strenght*tick_lenght
            if res := self.player.check_if_ground():
                self.player.grav_speed = 0
            # self.player.move((0, self.player.grav_speed))
            print(self.player.grav_speed, res, self.player.get_pos(), self.player.key_jump)
            
        
        if self.player.key_jump and self.player.check_if_ground():
            self.player.speed_y -= 100
            self.player.key_jump = False
            print("jumped")
            
        # self.player.gravity()
        # self.player.move((0,self.player.grav_speed*tick_lenght) )




        self.player.move((self.player.speed_x*tick_lenght, self.player.speed_y*tick_lenght))
        # print(self.player.check_if_ground())
        for entity in self.entities:
            entity.move((32*tick_lenght, 0))
        
        
        
        
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
        # print(recursion_depth)
        if recursion_depth >= 50:
            self.__pos[0] -= movement[0]
            self.__pos[1] -= movement[1]
            return
        if pygame.sprite.spritecollideany(self, self.world_engine.block_sprite_group) and recursion_depth <50:
            self.__pos[0] -= movement[0]
            self.__pos[1] -= movement[1]
            self.move((movement[0]-np.sign(movement[0]), movement[1]-np.sign(movement[1])), recursion_depth=recursion_depth+1)
            
    def get_pos(self) -> tuple:
        return self.__pos
    
    def check_if_ground(self) -> bool:
        self.__pos[1] += 1
        self.update_rect()
        if pygame.sprite.spritecollideany(self, self.world_engine.block_sprite_group):
            self.__pos[1] -= 1
            return True
        else:
            self.__pos[1] -=1
            return False
            

class Player(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, pos: tuple, size: tuple, image: pygame.image) -> None:
        super().__init__(wordlengine_ref, pos, size, image)
        self.speed_x = 0
        self.speed_y = 0
        self.key_jump = True
        self.time_since_in_air = 0
        self.grav_speed = 0

    def gravity(self) -> int:
        if not self.check_if_ground():
            if self.time_since_in_air == 0:
                self.time_since_in_air = time.time()
            time_now = time.time()
            grav_time = time_now - self.time_since_in_air
            self.grav_speed = settings.grav_strenght **grav_time
            print(self.grav_speed)
        else:
            self.time_since_in_air = 0
        
    
class Enemies(Entity):
     def __init__(self) -> None:
        pass
    