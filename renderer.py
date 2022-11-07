from typing import Tuple
import pygame
import math

import settings
import assets
from main import Game
from world import WorldEngine

class Renderer:
    def __init__(self,* , game_engine_ref:Game ,world_engine_ref:WorldEngine) -> None:
        self.game = game_engine_ref
        self.wold_engine = world_engine_ref
        self.camera_ofset = [0,0]
        pygame.font.init()
        self.debug_font = pygame.font.SysFont("Calibri", 15)
    
        self.screen = self.game.screen
        
        self.debug_screen = pygame.Surface((300, 500), flags=pygame.SRCALPHA)
        
        self.block_choices_screen = pygame.Surface((settings.blocksize, len(settings.block_choices)*settings.blocksize), flags=pygame.SRCALPHA)
        self.block_choices_screen_update()

        
        
    
    def draw(self):
        # self.screen.fill((0,0,0,0)) # Falls wir den Renderer Surface und den von dem Game trennen wollen
        self.blit_world()
        self.blit_entities()
        self.blit_player()
        
        if settings.render_walls:
            self.blit_walls()
        
        if self.game.world_edit_mode:
            self.screen.blit(self.block_choices_screen, settings.block_choices_screen_ofsett)
        
        if self.game.debug_mode:
            self.debu_menu_update()
            self.screen.blit(self.debug_screen, (10,10))
    
    def blit_world(self) -> None:
        for block in self.wold_engine.block_list:
            block_x = block[0][0]
            block_y = block[0][1]
            block_value = block[1]
            
            block_position = block_x*settings.blocksize-self.camera_ofset[0], block_y*settings.blocksize-self.camera_ofset[1]
            self.screen.blit(assets.textureMap[block_value], block_position)

    def blit_walls(self):
        for wall in self.wold_engine.walls:
            wall.draw(self.screen, self.camera_ofset)
            
    def debu_menu_update(self):
        self.debug_screen.fill((0,0,0,0))
        fpsText = self.debug_font.render(f"FPS : {round(self.game.clock.get_fps(),3)}", False, 6)
        self.debug_screen.blit(fpsText, (0,0))
        for entityNr, entity in enumerate(self.game.physics_engine.entities):
            entity_text = self.debug_font.render(f"Entity - Pos:{round(entity.pos[0], 2)}|{round(entity.pos[1], 2)}", False, 6)
            self.debug_screen.blit(entity_text, (0, 10 + 10*entityNr))
            
    def blit_entities(self):
        for entity in self.game.physics_engine.entities:
            self.blit_element(entity.image, entity.pos)

    def blit_player(self):
        self.blit_element(self.game.physics_engine.player.image, self.game.physics_engine.player.pos)

    def blit_element(self, element:pygame.surface or pygame.image, position:Tuple[int, int]) -> None:
        """ 
        !!! Die Position ist in Pixel und nicht in weltblöcken !!!
        Das Element wird an der Position korospondierend zu der Welt gerendert. 
        """
        self.screen.blit(element, [a-b for a,b in zip(position,self.camera_ofset)])
        
    def get_world_block_for_mouse_pos(self, mouse_pos:tuple) -> tuple:
        mouse_x, mouse_y = mouse_pos
        
        mouse_x -= self.camera_ofset[0]
        mouse_y -= self.camera_ofset[1]
        
        mouse_x //= settings.blocksize
        mouse_y //= settings.blocksize
        
        return mouse_x, mouse_y
        
    def block_choices_screen_update(self):
        self.block_choices_screen.fill((0,0,0,0))
        for index, block in enumerate(settings.block_choices):
            self.block_choices_screen.blit(assets.textureMap[block], (0, index*settings.blocksize))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (0,0), (settings.blocksize,0))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (0,0), (0,settings.blocksize*len(settings.block_choices)-1))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (0,settings.blocksize*len(settings.block_choices)-1), (settings.blocksize-1,settings.blocksize*len(settings.block_choices)-1))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (settings.blocksize-1,0), (settings.blocksize-1,settings.blocksize*len(settings.block_choices)-1))
            
    def block_choices_screen_get_clicked(self, mouse_pos:tuple):
        relateive_mouse_pos = [mouse - ofsett for mouse, ofsett in zip(mouse_pos, settings.block_choices_screen_ofsett)]
        block = math.floor(relateive_mouse_pos[1] / settings.blocksize)
        print(f"{relateive_mouse_pos=} , {block=}")
        return settings.block_choices[block]

        
    def block_choices_get_if_clicked_on(self, mouse_pos:tuple) -> bool:
        relateive_mouse_pos = [mouse - ofsett for mouse, ofsett in zip(mouse_pos, settings.block_choices_screen_ofsett)]
        clicked = self.block_choices_screen.get_rect().collidepoint(relateive_mouse_pos)
        print(clicked)
        return clicked