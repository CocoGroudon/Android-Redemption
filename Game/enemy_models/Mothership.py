import math
import random
from physics import Enemy
import assets

from enemy_models import Ball

class Mothership(Enemy):
    image = assets.enemies['mothership']
    movement_speed = 0
    size = image.get_size()
    gravity = False
    max_helth = 1000
    spawn_chance = 10000 # the higher the number the lower the chance
    
    def __init__(self, wordlengine_ref, physicsengine_ref, pos: tuple) -> None:

        super().__init__(wordlengine_ref, physicsengine_ref, pos, self.size, self.image)
        
        self.health.max = self.max_helth
        self.health.reset()
        
    def spawn_enemy(self):
        pos = self.get_pos()
        ball = Ball.Ball(self.world_engine, self.physics_engine, (pos[0] + self.size[0] / 2, pos[1] + self.size[1] / 2))
        self.physics_engine.add_enemie(ball)
    
    def action(self, tick_lenght: float):
        for _ in range(math.floor(1/tick_lenght/10)):
            rand = random.randint(0, self.spawn_chance)
            if rand == 0:
                self.spawn_enemy()
        