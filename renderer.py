import settings
import assets

class Renderer:
    def __init__(self,* , game_engine_ref ,world_engine_ref) -> None:
        self.game = game_engine_ref
        self.wold_engine = world_engine_ref
    
    def blitworld(self):
        for xIndex, xList in enumerate(self.wold_engine.world):
            for yIndex, block in enumerate(xList):
                block_position = xIndex*settings.blocksize, yIndex*settings.blocksize
                self.game.screen.blit(assets.textureMap[block], block_position)
