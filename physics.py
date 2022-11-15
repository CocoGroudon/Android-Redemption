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
                self.player.speed_y = 0
            # print(self.player.speed_y, res, self.player.get_pos(), self.player.key_jump)
            
        
        if self.player.key_jump and self.player.check_if_ground():
            self.player.speed_y -= settings.player_jump_strength
            

        self.player.move((0, self.player.speed_y*tick_lenght))
        self.player.move((self.player.speed_x*tick_lenght, 0))
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
        self.key_jump = False
        self.time_since_in_air = 0 
        self.inventory = Inventory()
    
class Item:
    def __init__(self, image) -> None:
        self.image = image
            
class Inventory:
    def __init__(self) -> None:
        self.__inventory_list:Item = [[None for j in range(settings.inventory_size[0])] for i in range(settings.inventory_size[1])]
        self.surface = pygame.Surface((settings.inventory_size[0]*settings.inventory_item_size, settings.inventory_size[1]*settings.inventory_item_size), flags=pygame.SRCALPHA)
        self.update_surface()
        
    def __get_first_empty_in_list(self, list:list) -> int:
        """ 
        returns the Index of the first position in a List, that is None \n
        If no Element of the List is None, the fuktion returns None
        """
        for index, cell in enumerate(list):
            if cell == None:
                return index
        return None
        
    def get_item(self, item_pos:tuple) -> Item or None:
        """ returns the item at the given position of the inventory or None if there is no item """
        item = self.__inventory_list[item_pos[0]][item_pos[1]]
        return item
    
    def add_item(self, item:Item) -> bool:
        """ 
        returned bool is: \n
        - True if the item was added succesfully \n
        - False if the item couldnt be added
        """
        lines_list = [None if self.__get_first_empty_in_list(line) != None else 1 for line in self.__inventory_list]
        first_empty_line = self.__get_first_empty_in_list(lines_list)
        if first_empty_line == None: 
            return False
        first_empty_col = self.__get_first_empty_in_list(self.__inventory_list[first_empty_line])
        
        print(f"added {item=} at position {first_empty_line} | {first_empty_col}")
        self.__inventory_list[first_empty_line][first_empty_col] = item
        
    def remove_item(self, position:tuple) -> None:
        self.__inventory_list[position[0]][position[1]] = None
                
    def update_surface(self):
        """ refreshes the surface / image of the Inventory """
        self.surface.fill((0,0,0,0))
        for col_index, line in enumerate(self.__inventory_list): # col_index and line_index are switched on purpose because of the was Python handles nested lists
            for line_index, cell in enumerate(line):
                if cell != None:
                    self.surface.blit(cell.image, (line_index*settings.inventory_item_size, col_index*settings.inventory_item_size))

                    
           
    
class Enemies(Entity):
     def __init__(self) -> None:
        pass
    