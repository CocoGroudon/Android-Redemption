import pygame
import settings
pygame.init()
pygame.display.init()

from scene import Scene


    
class Window:
    screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)
    isRunning = True
    
    def __init__(self) -> None:
        
        self.clock = pygame.time.Clock()
        self.scenes: Scene = {}
        self.current_scene:Scene = None

        from game import Game, play_mode, Mode_Edit
        from main_menu import Main_Menu

        self.game_scene = Game(window_manager=self)
        self.game_scene = play_mode(self.game_scene)
        self.scenes["game"] = self.game_scene

        
        self.main_menu_scene = Main_Menu(window=self)
        self.scenes["menu"] = self.main_menu_scene
        
        self.current_scene = self.scenes["menu"]
    
    def filter_events(self, events):
        myEvents = []
        for event in events:
            if event.type == pygame.QUIT:
                self.isRunning = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_0:
                    self.current_scene = self.scenes["menu"]
                elif event.key == pygame.K_KP_1:
                    self.current_scene = self.scenes["game"]
            myEvents.append(event)
        return myEvents
    
    def run(self):
        while self.isRunning:
            # print(self.clock.get_fps())
            events = self.filter_events(pygame.event.get())
            
            self.current_scene.update()
            self.current_scene.draw()
            self.current_scene.handle_events(events=events)
            
            pygame.display.flip()
            self.clock.tick(settings.framerate)
        for sceene in self.scenes:
            sceene.shutdown()
            
            
if __name__ == "__main__":
    window = Window()
    window.run()