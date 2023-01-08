import pygame

from scene import Scene

class Pause_Menu(Scene):
    def __init__(self, window, game):
        super().__init__(window)
        self.game = game
        # Werte sind egal
        self.size = (0,0)
        self.rebuild_screen(self.size)
        
        
    def rebuild_screen(self, new_size: tuple[int, int]):
        self.screen = pygame.surface.Surface(new_size, pygame.SRCALPHA)
        self.screen.fill((255, 255, 0, 50))
        
    def draw(self):
        window_size = self.window.screen.get_size()
        if window_size != self.size:
            self.rebuild_screen(window_size)
        self.game.draw()
        self.window.screen.blit(self.screen, (0, 0))
        # self.window.screen.fill((255,255, 0, 50))
        