import pygame
import random
import assets
import settings
from physics import Item, WorldEngine, Projectile, Projectile_Gravity

global projectile_amount
global projectile_inaccuracy
global damage

projectile_amount = 1
projectile_inaccuracy = 0.8 #in radiants
projectile_speed = 400
shoot_cooldown = 10 #time in ms
damage = 2
image = assets.texture_item["Flamethrower"]

def shoot(player, angle:float = 0):
    '''creates a new standart projectile in the given direction \n
    angle *must* be given in radiants, else everythin gets scuffed'''
    projectile = Projectile_Gravity(player, angle, player.get_pos()[:], settings.projectile_speed, 10)
    player.physics_engine.projectile_group.add(projectile)

class Flamethrower(Item):
    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref, pos: tuple) -> None:
        size = settings.item_size
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image, self.my_action)
    
    def my_action(self, angle:float = 0):
        time_since_shoot = pygame.time.get_ticks() - self.physics_engine.player.last_shot 
        print(time_since_shoot)
        if time_since_shoot < shoot_cooldown:
            return
        
        for _ in range(projectile_amount):
            new_angle = angle + (random.random() - 0.5) * projectile_inaccuracy
            origin_pos = [self.physics_engine.player.get_pos()[i] - settings.hand_ofsett[i] for i in range(2)]
            projectile = Projectile_Gravity(self.physics_engine.player, new_angle, origin_pos, projectile_speed, damage)
            self.physics_engine.projectile_group.add(projectile)
            self.physics_engine.player.last_shot = pygame.time.get_ticks()

# class Weapon(Item):
#     def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref, pos: tuple, size: tuple, image: pygame.image, action: callable = None) -> None:
#         super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image, action)