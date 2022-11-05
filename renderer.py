from typing import Tuple
import pygame

import settings
import assets
from main import Game
from world import WorldEngine

class Renderer:
    def __init__(self,* , game_engine_ref:Game ,world_engine_ref:WorldEngine) -> None:
        self.game = game_engine_ref
        self.wold_engine = world_engine_ref
        self.camera_ofset = [0,0]
        
        self.screen = self.game.screen
        self.debug_screen = pygame.Surface((300, 500), flags=pygame.SRCALPHA)
        
        pygame.font.init()
        self.debug_font = pygame.font.SysFont("Calibri", 30)
    
    def draw(self):
        # self.screen.fill((0,0,0,0)) # Falls wir den Renderer Surface und den von dem Game trennen wollen
        self.blit_world()
        self.blit_walls()
        
        self.debu_menu_update()
        self.screen.blit(self.debug_screen, (10,10))
    
    def blit_world(self) -> None:
        for block in self.wold_engine.block_list:
            block_x = block[0][0]
            block_y = block[0][1]
            block_value = block[1]
            
            block_position = block_x*settings.blocksize+self.camera_ofset[0], block_y*settings.blocksize+self.camera_ofset[1]
            self.screen.blit(assets.textureMap[block_value], block_position)

    def blit_walls(self):
        for wall in self.wold_engine.walls:
            wall.draw(self.screen, self.camera_ofset)
            
    def debu_menu_update(self):
        self.debug_screen.fill((0,0,0,0))
        fpsText = self.debug_font.render(f"FPS : {round(self.game.clock.get_fps(),3)}", False, 8)
        self.debug_screen.blit(fpsText, (0,0))
        
            
    def blit_element(self, element:pygame.surface or pygame.image, position:Tuple[int, int]) -> None:
        """ 
        !!! Die Position ist in Pixel und nicht in weltblöcken !!!
        Das Element wird an der Position korospondierend zu der Welt gerendert. 
        """
        self.screen.blit(element, [a+b for a,b in zip(position,self.camera_ofset)])
    