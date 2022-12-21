import pygame

from scene import Scene

class Main_Menu(Scene):
    def draw(self):
        self.window.screen.fill((255,255,255))
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.window.isRunning = False
            
