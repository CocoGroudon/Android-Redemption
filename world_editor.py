import pygame

import assets
import settings
import world
import renderer
import physics


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        
        self.world_engine = world.WorldEngine()
        self.world_engine.load_world_from_memory()
        
        self.render_engine = Renderer(game_engine_ref=self, world_engine_ref=self.world_engine)
        self.move_speed = 10
        
        self.world_edit_current_block = 1
        
        
    def draw(self):
        self.screen.fill((settings.backgroundcolor))
        self.render_engine.draw()
        
        
    def handle_keyinputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == settings.keybinds["toggle_fullscreen"]:
                    pygame.display.toggle_fullscreen()
                elif event.key in settings.keybinds["up"]:
                    self.render_engine.cam_ofset_y -= self.tick_lenght*self.move_speed
                elif event.key in settings.keybinds["left"]:
                    self.render_engine.cam_ofset_x -= self.tick_lenght*self.move_speed
                elif event.key in settings.keybinds["down"]:
     
                    self.render_engine.cam_ofset_y += self.tick_lenght*self.move_speed
                elif event.key in settings.keybinds["right"]:
                    self.render_engine.cam_ofset_y -= self.tick_lenght*self.move_speed



            elif event.type == pygame.KEYUP:
                pass
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # if self.render_engine.block_choices_get_if_clicked_on(mouse_pos): # Spieler hat auf das Menu geklickt
                #     self.world_edit_current_block = self.render_engine.block_choices_screen_get_clicked(mouse_pos)
                #     return
                # block_pos = self.render_engine.get_world_block_for_mouse_pos(mouse_pos)
                # self.world_engine.set_block(block_pos, self.world_edit_current_block)
                # self.world_engine.refresh_block_group()

    def event_shutdown(self):
        self.world_engine.save_world_to_memory()

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handle_keyinputs()
            self.draw()    
            pygame.display.flip()
            self.clock.tick(settings.framerate)
            if clock := self.clock.get_fps():
                self.tick_lenght = 1/clock
        self.event_shutdown()
        
class Renderer:
    def __init__(self, game_engine_ref:Game, world_engine_ref) -> None:
        self.game = game_engine_ref
        self.world_engine = world_engine_ref
        self.cam_ofset_y = 0
        self.cam_ofset_x = 0
        
        self.world_surface = pygame.surface.Surface((50*settings.blocksize,20*settings.blocksize))
        
    def draw(self):
        pass
        

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()