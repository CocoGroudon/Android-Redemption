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
        
        self.world_screen = pygame.Surface((settings.world_dimensions[0]*settings.blocksize, settings.world_dimensions[1]*settings.blocksize), flags=pygame.SRCALPHA)
        self.update_world_surface()
        
        self.debug_screen = pygame.Surface((300, 500), flags=pygame.SRCALPHA)
        self.screen_ofsettles = pygame.Surface((settings.world_dimensions[0]*settings.blocksize, settings.world_dimensions[1]*settings.blocksize), flags=pygame.SRCALPHA)
        
        self.block_choices_screen = pygame.Surface((settings.blocksize, len(settings.block_choices)*settings.blocksize), flags=pygame.SRCALPHA)
        self.block_choices_screen_update()

        
    
    def draw(self):
        # self.screen.fill((0,0,0,0)) # Falls wir den Renderer Surface und den von dem Game trennen wollen
        self.screen_ofsettles.fill((0,0,0,0))
        self.blit_world()
        self.blit_entities()
        self.blit_player()
        self.blit_player_inventory()
        self.blit_projectiles()
                
        if self.game.world_edit_mode:
            self.screen.blit(self.block_choices_screen, settings.block_choices_screen_ofsett)
        
        if self.game.debug_mode:
            self.debu_menu_update()
            self.screen.blit(self.debug_screen, (10,10))
    
    def blit_world(self) -> None:
        self.screen.blit(self.world_screen, self.camera_ofset)
    
    def update_world_surface(self):
        self.world_screen.fill((0,0,0,0))
        self.wold_engine.block_sprite_group.draw(self.world_screen)
           
    def debu_menu_update(self):
        self.debug_screen.fill((0,0,0,0))
        fpsText = self.debug_font.render(f"FPS : {round(self.game.clock.get_fps(),3)}", False, 6)
        self.debug_screen.blit(fpsText, (0,0))
        # for entityNr, entity in enumerate(self.game.physics_engine.entities):
        #     entity_text = self.debug_font.render(f"Entity - Pos:{round(entity.get_pos()[0], 2)}|{round(entity.get_pos()[1], 2)}", False, 6)
        #     self.debug_screen.blit(entity_text, (0, 10 + 10*entityNr))
            
    def blit_entities(self):
        self.game.physics_engine.entity_group.draw(self.screen_ofsettles)
        # for entity in self.game.physics_engine.entities:
            # self.blit_element(entity.image, entity.get_pos())

    def blit_player(self):
        self.blit_element(self.game.physics_engine.player.image, self.game.physics_engine.player.get_pos())

    def blit_player_inventory(self):
        self.blit_element(self.game.physics_engine.player.inventory.surface, self.game.physics_engine.player.get_pos())

    def blit_projectiles(self):
        self.game.physics_engine.projectile_group.draw(self.screen_ofsettles)
        self.screen.blit(self.screen_ofsettles, self.camera_ofset)

    def blit_element(self, element:pygame.surface or pygame.image, position:tuple[int, int]) -> None:
        """ 
        !!! Die Position ist in Pixel und nicht in weltblöcken !!!
        Das Element wird an der Position korospondierend zu der Welt gerendert. 
        """
        self.screen.blit(element, [a+b for a,b in zip(position,self.camera_ofset)])
        
    def get_world_block_for_mouse_pos(self, mouse_pos:tuple) -> tuple:
        mouse_x, mouse_y = mouse_pos
        
        mouse_x -= self.camera_ofset[0]
        mouse_y -= self.camera_ofset[1]
        
        mouse_x //= settings.blocksize
        mouse_y //= settings.blocksize
        
        # Keine Ahnung, warumm das da oben nicht automatisch in nen int macht, wenn es doch eh rundet
        mouse_x = int(mouse_x)
        mouse_y = int(mouse_y)
        
        return mouse_x, mouse_y
        
    def get_world_pos_for_mouse_pos(self, mouse_pos:tuple) -> tuple:
        mouse_x, mouse_y = mouse_pos
        
        mouse_x -= self.camera_ofset[0]
        mouse_y -= self.camera_ofset[1]
        
        return mouse_x, mouse_y
    
    def get_screen_pos_for_world_pos(self, world_pos:tuple) -> tuple:
        player_x, player_y = world_pos
        cam_ofset_x, cam_ofset_y = self.camera_ofset
        
        player_screen_x = player_x + cam_ofset_x
        player_screen_y = player_y + cam_ofset_y
        return player_screen_x, player_screen_y
    
    
    
        
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
    
    def update_camera_pos(self, player_pos:tuple):
        cam_pos_x, cam_pos_y = -player_pos[0]+self.screen.get_width()//2, -player_pos[1]+self.screen.get_height()//2

        if cam_pos_x > 0:
            cam_pos_x = 0
        elif cam_pos_x < -settings.world_dimensions[0]*settings.blocksize+self.screen.get_width():
            cam_pos_x = -settings.world_dimensions[0]*settings.blocksize+self.screen.get_width()
            
        if cam_pos_y > 0:
            cam_pos_y = 0
        elif cam_pos_y < -settings.world_dimensions[1]*settings.blocksize+self.screen.get_height():
            cam_pos_y = -settings.world_dimensions[1]*settings.blocksize+self.screen.get_height()
            
        self.camera_ofset = cam_pos_x, cam_pos_y
        