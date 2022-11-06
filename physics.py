import pygame
import math

import assets
import settings
from world import WorldEngine, Wall


class Physics:
    def __init__(self, worldengine_ref:WorldEngine) -> None:
        self.world_engine = worldengine_ref
        self.entities: Entity = []
        self.entities.append(Entity(self.world_engine, (80,150), (16,16), assets.textureMap["test_entity"]))
        self.entities.append(Entity(self.world_engine, (0,0), (16,16), assets.textureMap["test_entity"]))
        
    def tick(self):
        for entity in self.entities:
            entity.move((-0.1, -0.1))

class Entity:
    def __init__(self, wordlengine_ref:WorldEngine, pos:tuple, size:tuple, image:pygame.image) -> None:
        self.world_engine = wordlengine_ref
        self.pos = pos
        self.size = size
        self.image = image         
        self.ray_ofsett = settings.entity_move_rays_ofsett
        self.pos_ray = Ray(self, (0,0))
        self.set_move_rays()
    
    def set_move_rays(self):
        ofsett = self.ray_ofsett
        top_left = Ray(self, (ofsett,ofsett))
        top_right = Ray(self, (self.size[0]-ofsett,ofsett))
        bottom_left = Ray(self, (ofsett,self.size[1]-ofsett))
        bottom_right = Ray(self, (self.size[0]-ofsett, self.size[1]-ofsett))
        self.move_rays = top_left, top_right, bottom_left, bottom_right
        
    def move(self, movement:tuple):
        angle = self.pos_ray.get_angle_for_movement(movement)
        move_len = self.pos_ray.get_len_for_movement(movement)
        record = None
        
        for ray in self.move_rays:
            dist = ray.get_dist_to_walls(self.world_engine.walls, move_len, angle)
            if dist:
                if record == None:
                    record = dist
                if dist < record:
                    record = dist
                    
        if record == None: #TODO: Es gibt keine Wand in die Richtung, eig sollte die Wand umrant sein 
            self.pos = self.pos_ray.get_pos_for_len(move_len, angle)
            return
            
        record = round(record, 2)
        if record == 0:
            return
        
        if record <move_len: # Spieler fliegt gegen Wand
            self.pos = self.pos_ray.get_pos_for_len(record- self.ray_ofsett, angle)
        else: 
            self.pos = self.pos_ray.get_pos_for_len(move_len, angle)
            
            
        

# class Player(Entity):
#     def __init__(self) -> None:
#         super().__init__((1,0))
#         self.print_pos()
    


# class Enemies():
#     def __init__(self) -> None:
#         pass
    
    
    
class Ray:
    def __init__(self, assigned_entity:Entity, pos_ofsett:tuple) -> None:
        self.pos_ofsett = pos_ofsett
        self.owner = assigned_entity
    
    def get_origin_pos(self) -> tuple: 
        x, y = self.owner.pos
        x += self.pos_ofsett[0]
        y += self.pos_ofsett[1]
        return x,y 
    
    def get_pos_for_len(self, len:float, angle:float) -> tuple:
        x, y = self.get_origin_pos()

        # find the end point
        endy = y + len * math.sin(math.radians(angle))
        endx = x + len * math.cos(math.radians(angle))
        return endx, endy

    def get_len_for_pos(self, pos:tuple) -> float:
        x, y = self.get_origin_pos()
        delta_x = pos[0]-x
        delta_y = pos[1]-y
        
        return math.sqrt(delta_x**2+delta_y**2) # Satz des Pythagoras
    
    def get_len_for_movement(self, movement:tuple) -> float:
        delta_x = movement[0]
        delta_y = movement[1]
        
        return math.sqrt(delta_x**2+delta_y**2) # Satz des Pythagoras
    
    def get_angle_for_pos(self, pos:tuple) -> float:
        x, y = self.get_origin_pos()
        delta_x = pos[0]-x
        delta_y = pos[1]-y

        angle = math.atan2(delta_y, delta_x)
        angle = (angle/math.pi*180)
        return angle
    
    def get_angle_for_movement(self, movement:tuple) -> float:
        delta_x = movement[0]
        delta_y = movement[1]

        angle = math.atan2(delta_y, delta_x)
        angle = (angle/math.pi*180)
        return angle

    def check_intersection_with_wall(self, wall:Wall, ray_len:int, angle:float) -> False or tuple:
        y1 = wall.y1
        x1 = wall.x1

        x2 = wall.x2
        y2 = wall.y2

        x3, y3= self.get_origin_pos()

        x4, y4 = self.get_pos_for_len(ray_len, angle)

        den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if den == 0:
            return False
        t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / den
        u = -((x1-x2) * (y1-y3) - (y1-y2) * (x1-x3)) / den

        if (t > 0 and t < 1 and u > 0): # falls es keinen Punkt gibt
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return x,y 
        else:
            return False

    def check_intersection_with_walls(self, walls, ray_len:int, angle:float) -> None or tuple:
        record_dis = math.inf 
        record_pos = None
        ray_pos = self.get_origin_pos()
        for wall in walls:
            if pos := self.check_intersection_with_wall(wall, ray_len, angle):
                dist = math.dist(ray_pos, pos)
                if dist < record_dis:
                    record_dis = dist
                    record_pos = pos
        return record_pos

    def get_dist_to_walls(self, walls, lenght:int, angle:float) -> False or float:
        wallcollision = self.check_intersection_with_walls(walls, lenght, angle)
        pos = self.get_origin_pos()
        if wallcollision:
            return math.dist(pos, wallcollision)
        return False

    def draw(self, screen:pygame.Surface):
        pos = self.get_origin_pos()
        pygame.draw.circle(screen, (120,120,200), pos, 5)
        pygame.draw.aaline(screen, (120,120,200), pos, self.get_pos_for_len(16, 0))
        