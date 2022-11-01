import pygame
import settings

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((500,500))

        self.framerate = settings.framerate
        self.backgroundcolor = settings.backgroundcolor

    def draw(self):
        self.screen.fill(self.backgroundcolor)
        
    def handle_keyinputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

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


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()