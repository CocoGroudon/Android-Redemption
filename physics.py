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
        
        self.projectile_group = pygame.sprite.Group()
        self.entity_group = pygame.sprite.Group()
        self.entity_group.add(
            Entity(self.world_engine, self, (80,64), (16,16), assets.textureMap["test_entity"]),
            Entity(self.world_engine, self, (40,40), (16,16), assets.textureMap["test_entity"]))
        self.player = Player(self.world_engine, self, (40,40), (32,64), assets.textureMap["player_entity"])


        self.items_group = pygame.sprite.Group()
        
    def tick(self):
        # Setup for Tick
        fps = self.game.clock.get_fps()
        if fps == 0: return
        tick_lenght = 1/fps

        self.handle_player(tick_lenght)
        self.handle_entities(tick_lenght)
        self.handle_projectiles(tick_lenght)

        self.collect_item()

    def handle_entities(self, tick_lenght):
        for entity in self.entity_group:
            will_die = False
            
            entity.move((3*tick_lenght, 20*tick_lenght))
                        
            if entity.health.check_if_dead():
                print("should die")
                will_die = True
                
            if will_die:
                self.entity_group.remove(entity)

    def handle_player(self, tick_lenght):
        if self.player.key_shoot:
            angle = get_angle_to_world_pos(self.player.get_pos(), self.game.render_engine.get_world_pos_for_mouse_pos(pygame.mouse.get_pos()))
            self.player.shoot(angle)
            self.player.key_shoot = False
            
        if settings.gravity:
            self.player.speed_y += settings.grav_strenght*tick_lenght
            if self.player.check_if_ground():
                self.player.speed_y = 0
                
        if self.player.key_jump and self.player.check_if_ground():
            self.player.speed_y -= settings.player_jump_strength
            
        self.player.move((0, self.player.speed_y*tick_lenght))
        self.player.move((self.player.speed_x*tick_lenght, 0))
            
    def handle_projectiles(self, tick_lenght:float):
        for projectile in self.projectile_group:
            projectile.move_forth(tick_lenght)
            will_die = False
            
            for entity in self.entity_group:
                if pygame.sprite.collide_rect(projectile, entity):
                    entity.health.take_damage(projectile.damage)
                    will_die = True
            
            if projectile.check_if_to_old(): 
                will_die = True
                
            if pygame.sprite.spritecollideany(projectile, self.world_engine.block_sprite_group):
                will_die = True
            
            if will_die: 
                self.projectile_group.remove(projectile)
        
    def new_item(self):
        item = Item(self.world_engine, self, (100, 100), (16,16), assets.textureMap["weed"])
        self.entity_group.add(item)
        self.items_group.add(item)

    def collect_item(self):
        for item in self.items_group:
            if self.player.rect.colliderect(item.rect):
                print("colliede with item")
                self.player.inventory.add_item(item)
                self.items_group.remove(item)
                self.entity_group.remove(item)

class Entity(pygame.sprite.Sprite):
    def __init__(self, wordlengine_ref:WorldEngine, physicsengine_ref:Physics, pos:tuple, size:tuple, image:pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.world_engine = wordlengine_ref
        self.physics_engine = physicsengine_ref
        self.__pos = list(pos)
        self.size = size
        self.image = image    
        self.update_rect()
        self.health = Health_Bar(100)

             
        
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
            
    def get_angle_to_world_pos(self, origin:tuple, destination:tuple) -> float:
        '''
        returned value is in arc tangent
        '''
        delta_x = origin[0]-destination[0]
        delta_y = origin[1]-destination[1]
        angle = math.atan2(delta_y, delta_x)
        return angle
            
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
    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref:Physics ,pos: tuple, size: tuple, image: pygame.image) -> None:
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image)
        self.speed_x = 0
        self.speed_y = 0
        self.key_jump = False
        self.time_since_in_air = 0 
        self.inventory = Inventory()
        self.key_shoot = False
        
    def shoot(self, angle:float):
        '''creates a new standart projectile in the given direction \n
        angle *must* be given in radiants, else everythin gets scuffed'''
        projectile = Projectile_Gravity(self, angle, self.get_pos()[:], settings.projectile_speed, 10)
        self.physics_engine.projectile_group.add(projectile)
        
    
class Item(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref, pos: tuple, size: tuple, image: pygame.image) -> None:
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image)
        self.image = image
        self.pos = pos
        self.size = size
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
    def __init__(self, owner:Entity, angle:float, start_pos:tuple, speed:float, damage:float) -> None:
        pygame.sprite.Sprite.__init__(self=self)
        self.pos_x, self.pos_y = start_pos
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.time_of_spawn = time.time()
                
        self.image_normal = assets.textureMap["projectile"]
        self.image = pygame.transform.rotate(self.image_normal, (math.degrees(self.angle)+180)*-1)
        self.rect = self.image.get_rect()
        
    def move_forth(self, tick_lenght:float):
        '''Advances the projectile Position the distance'''
        dist = self.speed*tick_lenght
        self.pos_x += dist*math.cos(self.angle)
        self.pos_y += dist*math.sin(self.angle)

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.pos_x, self.pos_y)
        
    def check_if_to_old(self) -> bool:
        ''' Returns weather the Sprite is older then the specified "projectile_lifetime" in settings '''
        existence_time = time.time() - self.time_of_spawn
        if existence_time > settings.projectile_lifetime:
            return True
        return False


class Projectile_Gravity(Projectile):  
    def __init__(self, owner: Entity, angle: float, start_pos: tuple, speed: float, damage:float) -> None:
        super().__init__(owner, angle, start_pos, speed, damage)
        self.down_speed = 0
    
    def move_forth(self, tick_lenght:float):
        self.down_speed += settings.grav_strenght*tick_lenght
        self.pos_y += self.down_speed*tick_lenght
        return super().move_forth(tick_lenght)
  
  
class Health_Bar:
    def __init__(self, max_Health:int) -> None:
        self.max = max_Health
        self.current = max_Health
        
    def take_damage(self, damage):
        self.current -= damage
    
    def heal(self, healing):
        self.current += healing
        if self.current > self.max:
            self.current = self.max
            
    def check_if_dead(self) -> bool:
        if self.current <= 0:
            return True
        return False
