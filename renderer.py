from typing import Tuple
import pygame
import settings
import assets

class Renderer:
    def __init__(self,* , game_engine_ref ,world_engine_ref) -> None:
        self.game = game_engine_ref
        self.wold_engine = world_engine_ref
        self.camera_ofsett = [0,0]
    
    def blit_world(self):
        for xIndex, xList in enumerate(self.wold_engine.world):
            for yIndex, block in enumerate(xList):
                block_position = xIndex*settings.blocksize+self.camera_ofsett[0], yIndex*settings.blocksize+self.camera_ofsett[1]
                self.game.screen.blit(assets.textureMap[block], block_position)

    def blit_element(self, element:pygame.surface or pygame.image, position:Tuple[int, int]) -> None:
        """ 
        !!! Die Position ist in Pixel und nicht in weltblöcken !!!
        Das Element wird an der Position korospondierend zu der Welt gerendert. 
        """
        self.game.screen.blit(element, [a+b for a,b in zip(position,self.camera_ofsett)])
    