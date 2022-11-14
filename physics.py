import pygame
import math
import numpy as np
import time

import assets
import settings
from world import WorldEngine

def get_angle_to_world_pos(origin:tuple, destination:tuple) -> float:
    '''
    returned value is in arc tangent
    '''
    delta_x = destination[0]-origin[0]
    delta_y = destination[1]-origin[1]
    angle = math.atan2(delta_y, delta_x)
    return angle

def get_world_pos_for_angle(starting_pos:tuple, angle:float, len:float):
    start_x, start_y = starting_pos
    
    end_x = start_x + len * math.cos(angle)
    end_y = start_y + len * math.sin(angle)
    
    return end_x, end_y


class Physics:
    def __init__(self, worldengine_ref:WorldEngine, game_ref) -> None:
        self.world_engine = worldengine_ref
        self.game = game_ref
        
        self.entities: Entity = []
        self.entities.append(Entity(self.world_engine, self, (80,64), (16,16), assets.textureMap["test_entity"]))
        self.entities.append(Entity(self.world_engine, self, (40,40), (16,16), assets.textureMap["test_entity"]))
        self.player = Player(self.world_engine, self, (40,40), (32,64), assets.textureMap["player_entity"])
        
        self.projectile_group = pygame.sprite.Group()

    def tick(self):
        fps = self.game.clock.get_fps()
        if fps == 0: return
        tick_lenght = 1/fps
        self.player.move((self.player.speed_x*tick_lenght, self.player.speed_y*tick_lenght))
        for entity in self.entities:
            entity.move((32*tick_lenght, 0))
            
        self.handle_projectiles(tick_lenght)

            
    def handle_projectiles(self, tick_lenght:float):
        for projectile in self.projectile_group:
            if projectile.check_if_to_old():
                self.projectile_group.remove(projectile)
            projectile.move_forth(settings.projectile_speed*tick_lenght)
            
        if self.player.key_shoot:
            angle = get_angle_to_world_pos(self.player.get_pos(), self.game.render_engine.get_world_pos_for_mouse_pos(pygame.mouse.get_pos()))
            self.player.shoot(angle)
            self.player.key_shoot = False
        
class Entity(pygame.sprite.Sprite):
    def __init__(self, wordlengine_ref:WorldEngine, physicsengine_ref:Physics, pos:tuple, size:tuple, image:pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.world_engine = wordlengine_ref
        self.physics_engine = physicsengine_ref
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
            # self.move((movement[0]-np.sign(movement[0]), movement[1]-np.sign(movement[1])), recursion_depth=recursion_depth+1)
            
    def get_angle_to_world_pos(self, origin:tuple, destination:tuple) -> float:
        '''
        returned value is in arc tangent
        '''
        delta_x = origin[0]-destination[0]
        delta_y = origin[1]-destination[1]
        angle = math.atan2(delta_y, delta_x)
        return angle
            
    def get_pos(self) -> tuple:
        return self.__pos

class Player(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref:Physics ,pos: tuple, size: tuple, image: pygame.image) -> None:
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image)
        self.speed_x = 0
        self.speed_y = 0
        self.inventory = Inventory()
        self.key_shoot = False
        
    def shoot(self, angle:float):
        '''creates a new standart projectile in the given direction \n
        angle *must* be given in radiants, else everythin gets scuffed'''
        projectile = Projectile(self, angle, self.get_pos()[:])
        self.physics_engine.projectile_group.add(projectile)
        
    
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

class Projectile(pygame.sprite.Sprite):
    '''A basic projectile that has no gravity and isn`t hitscan'''
    def __init__(self, owner:Entity, angle:float, start_pos:tuple) -> None:
        pygame.sprite.Sprite.__init__(self=self)
        self.starting_pos = start_pos
        self.pos = start_pos
        self.angle = angle
        self.time_of_spawn = time.time()
                
        self.image_normal = assets.textureMap["test_projectile"]
        self.image_rotated = pygame.transform.rotate(self.image_normal, (math.degrees(self.angle)+180)*-1)
        
        self.rect = self.image_rotated.get_rect()
        self.dist_traveled = 0
        
    def move_forth(self, dist:float):
        '''Advances the projectile Position the distance'''
        self.dist_traveled += dist
        new_x = self.starting_pos[0]+self.dist_traveled*math.cos(self.angle)
        new_y = self.starting_pos[1]+self.dist_traveled*math.sin(self.angle)

        self.pos = new_x, new_y
        self.rect = self.image_rotated.get_rect()
        self.rect = self.rect.move(self.pos[0], self.pos[1])
        
    def check_if_to_old(self) -> bool:
        ''' Returns weather the Sprite is older then the specified "projectile_lifetime" in settings '''
        existence_time = time.time() - self.time_of_spawn
        if existence_time > settings.projectile_lifetime:
            return True
        return False
    
class Enemies(Entity):
     def __init__(self) -> None:
        pass
    