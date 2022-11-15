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
        self.framerate = settings.framerate
        self.backgroundcolor = settings.backgroundcolor
        
        self.world_engine = world.WorldEngine()
        self.world_engine.load_world_from_memory()
        self.render_engine = renderer.Renderer(game_engine_ref=self, world_engine_ref=self.world_engine)
        self.physics_engine = physics.Physics(self.world_engine, self)
        
        self.world_edit_mode = True
        self.world_edit_current_block = 1
        
        self.debug_mode = True

    def draw(self):
        self.screen.fill((settings.backgroundcolor))
        self.render_engine.draw()
        
        # self.render_engine.blit_element(assets.textureMap["test_entity"], self.physics_engine.entities[0].pos)

    def handle_keyinputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == settings.keybinds["toggle_fullscreen"]:
                    pygame.display.toggle_fullscreen()
                elif event.key in settings.keybinds["up"]:
                    self.physics_engine.player.key_jump = True
                elif event.key in settings.keybinds["left"]:
                    self.physics_engine.player.speed_x -= 128
                elif event.key in settings.keybinds["down"]:
                    self.physics_engine.new_item()
                elif event.key in settings.keybinds["right"]:
                    self.physics_engine.player.speed_x += 128
                elif event.key in settings.keybinds["action"]:
                    self.physics_engine.player.key_shoot = True
            elif event.type == pygame.KEYUP:
                if event.key in settings.keybinds["up"]:
                    self.physics_engine.player.key_jump = False
                    
                elif event.key in settings.keybinds["left"]:
                    self.physics_engine.player.speed_x += 128
                elif event.key in settings.keybinds["down"]:
                    pass
                elif event.key in settings.keybinds["right"]:
                    self.physics_engine.player.speed_x -= 128
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.world_edit_mode:
                    if self.render_engine.block_choices_get_if_clicked_on(mouse_pos): # Spieler hat auf das Menu geklickt
                        self.world_edit_current_block = self.render_engine.block_choices_screen_get_clicked(mouse_pos)
                        return
                    block_pos = self.render_engine.get_world_block_for_mouse_pos(mouse_pos)
                    print(block_pos)
                    self.world_engine.set_block(block_pos, self.world_edit_current_block)
                    self.world_engine.refresh_block_group()
                    self.render_engine.update_world_surface()

    def event_shutdown(self):
        self.world_engine.save_world_to_memory()

    def run(self):
        self.__run()

    def stop(self):
        self.isRunning = False

    def __run(self):
        self.isRunning = True
        while self.isRunning:
            self.handle_keyinputs()
            self.render_engine.update_camera_pos(self.physics_engine.player.get_pos())
            self.draw()    
            self.physics_engine.tick()
            pygame.display.flip()
            self.clock.tick(settings.framerate)
        self.event_shutdown()


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()