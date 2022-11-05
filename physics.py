import settings
import pygame

class Physics:
    def __init__(self) -> None:
        self.player = Player()
        
        self.jump = False

class Entity:
    def __init__(self, pos:tuple) -> None:
        self.pos = pos
        pass
    
    def print_pos(self):
        print(self.pos)

class Player(Entity):
    def __init__(self) -> None:
        super().__init__((1,0))
        self.print_pos()
    


class Enemies():
    def __init__(self) -> None:
        pass