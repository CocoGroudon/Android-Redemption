import pygame
import settings
import world
import renderer

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)
        self.world_engine = world.WorldEngine()
        self.render_engine = renderer.Renderer(game_engine_ref=self, world_engine_ref=self.world_engine)

        self.framerate = settings.framerate
        self.backgroundcolor = settings.backgroundcolor

    def draw(self):
        self.screen.fill(self.backgroundcolor)
        self.render_engine.blit_world()
        
    def handle_keyinputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == settings.keybinds["toggle_fullscreen"]:
                    pygame.display.toggle_fullscreen()
                elif event.key == settings.keybinds["up"]:
                    self.render_engine.camera_ofsett[1] -= 16
                elif event.key == settings.keybinds["left"]:
                    self.render_engine.camera_ofsett[0] -= 16
                elif event.key == settings.keybinds["down"]:
                    self.render_engine.camera_ofsett[1] += 16
                elif event.key == settings.keybinds["right"]:
                    self.render_engine.camera_ofsett[0] += 16
        
    def event_shutdown(self):
        self.world_engine.save_world_to_memory()

    def run(self):
        self.__run()

    def stop(self):
        self.isRunning = False

    def __run(self):
        self.isRunning = True
        clock = pygame.time.Clock()
        while self.isRunning:
            self.handle_keyinputs()
            self.draw()    
            pygame.display.flip()
            clock.tick(self.framerate)
        self.event_shutdown()


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()