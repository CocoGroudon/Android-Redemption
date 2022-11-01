from typing import Tuple
import pygame
from main import Game
import settings
import assets
from world import WorldEngine

class Renderer:
    def __init__(self,* , game_engine_ref:Game ,world_engine_ref:WorldEngine) -> None:
        self.game = game_engine_ref
        self.wold_engine = world_engine_ref
        self.camera_ofset = [0,0]
    
    def blit_world(self) -> None:
        for xIndex, xList in enumerate(self.wold_engine.world):
            for yIndex, block in enumerate(xList):
                block_position = xIndex*settings.blocksize+self.camera_ofset[0], yIndex*settings.blocksize+self.camera_ofset[1]
                self.game.screen.blit(assets.textureMap[block], block_position)

    def blit_element(self, element:pygame.surface or pygame.image, position:Tuple[int, int]) -> None:
        """ 
        !!! Die Position ist in Pixel und nicht in weltblöcken !!!
        Das Element wird an der Position korospondierend zu der Welt gerendert. 
        """
        self.game.screen.blit(element, [a+b for a,b in zip(position,self.camera_ofset)])
    