import pygame
import pstats
import cProfile
import time
import os, sys
import json

import assets 
import settings as settings
import world as world
import renderer as renderer
import physics as physics
import trigger_zone_models

from enemy_models import Ball

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        filename = os.path.basename(filename)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


class Game:
    def __init__(self) -> None:
        self.screen = assets.screen
        self.clock = pygame.time.Clock()
        
        self.world_engine = world.WorldEngine(self)

        self.render_engine = renderer.Renderer(game_engine_ref=self, world_engine_ref=self.world_engine)
        self.physics_engine = physics.Physics(self.world_engine, self)
        
        self.world_edit_current_block = 1
        

    def draw(self):
        self.screen.fill((settings.backgroundcolor))
        self.render_engine.draw()
        
    def build_trigger_zones_for_room(self, room_name:str, ofsett:int):
        '''ofsett is the ofsett from the left side of the world'''
        myzones = []
        with open(find_data_file(f"rooms/{room_name}/trigger_zones.json"), "r") as file:
            data = json.load(file)
            print(data)
            for zone in data:
                zone_type = zone["type"]
                zone_model = trigger_zone_models.zones[zone_type]
                atributes = zone["attributes"]
                myzone = zone_model(self.world_engine, self.physics_engine, **atributes, ofsett=ofsett)
                myzones.append(myzone)
        self.physics_engine.trigger_zones += myzones
        
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
                    self.physics_engine.player.move_speed_x -= 128
                elif event.key in settings.keybinds["down"]:
                    self.physics_engine.new_item()
                elif event.key in settings.keybinds["right"]:
                    self.physics_engine.player.move_speed_x += 128
                elif event.key in settings.keybinds["action"]:
                    self.physics_engine.player.inventory.get_hand_item().reset_pick_up_delay()
                    self.physics_engine.discard_item()
                elif event.key in settings.keybinds["inventory"]:
                    self.render_engine.inventory_show = not self.render_engine.inventory_show  
                elif event.key == pygame.K_2:
                    enemy = Ball.Ball(self.world_engine, self.physics_engine, (50,50))
                    self.physics_engine.add_enemie(enemy)
            elif event.type == pygame.KEYUP:
                if event.key in settings.keybinds["up"]:
                    self.physics_engine.player.key_jump = False
                elif event.key in settings.keybinds["left"]:
                    self.physics_engine.player.move_speed_x += 128
                elif event.key in settings.keybinds["right"]:
                    self.physics_engine.player.move_speed_x -= 128
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                hand_item = self.physics_engine.player.inventory.get_hand_item()
                self.physics_engine.player.key_shoot = True
                if issubclass(type(hand_item), physics.Weapon):
                    hand_item.time_since_shoot = time.time()-hand_item.shoot_cooldown-1
                
                if self.render_engine.inventory_get_clicked(mouse_pos) and self.render_engine.inventory_show:
                    self.physics_engine.player.inventory.hand = self.render_engine.inventory_get_clicked_pos(mouse_pos)
                elif settings.world_edit_mode:
                    if self.render_engine.block_choices_get_if_clicked_on(mouse_pos): # Spieler hat auf das Menu geklickt
                        self.world_edit_current_block = self.render_engine.block_choices_screen_get_clicked(mouse_pos)
                        return
                    block_pos = self.render_engine.get_world_block_for_mouse_pos(mouse_pos)
                    print(block_pos)
                    self.world_engine.set_block(block_pos, self.world_edit_current_block)
                    self.world_engine.refresh_block_group()
                    self.render_engine.update_world_surface()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.physics_engine.player.key_shoot = False

    def event_shutdown(self):
        pass

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handle_keyinputs()
            self.render_engine.update_camera_pos(self.physics_engine.player.get_pos())
            self.draw()    
            self.physics_engine.tick()
            pygame.display.flip()
            self.clock.tick(settings.framerate)
        self.event_shutdown()

class Game_Editor(Game):
    def __init__(self) -> None:
        super().__init__()
        settings.gravity = False
        self.physics_engine.player.force_y = 0
        
    
    def handle_keyinputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == settings.keybinds["toggle_fullscreen"]:
                    pygame.display.toggle_fullscreen()
                elif event.key in settings.keybinds["up"]:
                    self.physics_engine.player.speed_y = -128
                elif event.key in settings.keybinds["left"]:
                    self.physics_engine.player.speed_x = -128
                elif event.key in settings.keybinds["down"]:
                    self.physics_engine.player.speed_y = 128
                elif event.key in settings.keybinds["right"]:
                    self.physics_engine.player.speed_x = 128
                elif event.key in settings.keybinds["action"]:
                    self.physics_engine.player.key_shoot = True
                    
                    
            elif event.type == pygame.KEYUP:
                if event.key in settings.keybinds["up"]:
                    self.physics_engine.player.speed_y = 0
                elif event.key in settings.keybinds["left"]:
                    self.physics_engine.player.speed_x = 0
                elif event.key in settings.keybinds["down"]:
                    self.physics_engine.player.speed_y = 0
                elif event.key in settings.keybinds["right"]:
                    self.physics_engine.player.speed_x = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.render_engine.block_choices_get_if_clicked_on(mouse_pos): # Spieler hat auf das Menu geklickt
                    self.world_edit_current_block = self.render_engine.block_choices_screen_get_clicked(mouse_pos)
                    return
                block_pos = self.render_engine.get_world_block_for_mouse_pos(mouse_pos)
                print(block_pos)
                self.world_engine.set_block(block_pos, self.world_edit_current_block)
                self.world_engine.refresh_block_group()
                self.render_engine.update_world_surface()

def edit_mode():
    settings.world_edit_mode = True
    room_name = str(input("wie soll der Raum heißen?: "))
    game = Game_Editor()
    
    try: 
        game.world_engine.load_room_from_memory(room_name)
    except FileNotFoundError:
        os.mkdir(f"{settings.dictPath}/rooms/{room_name}")
        x = int(input("wie breit soll der Raum werden?: "))
        y = int(input("wie hoch soll der Raum werden?: "))
        game.world_engine.set_new_room((x,y)) 

    game.world_engine.refresh_block_group()
    game.render_engine.update_world_surface()
    game.run()
    game.world_engine.save_room_to_memory(room_name)

def play_mode():
    game = Game()
    game.world_engine.create_new_random_world(0)

    from item_models import Flamethrower
    flamethrower = Flamethrower.Flamethrower(game.world_engine, game.physics_engine, game.physics_engine.player.get_pos())
    game.physics_engine.player.inventory.add_item(flamethrower)
    from item_models import Deagle
    deagle = Deagle.Deagle(game.world_engine, game.physics_engine, game.physics_engine.player.get_pos())
    game.physics_engine.player.inventory.add_item(deagle)
    from item_models import Shotgun
    shotgun = Shotgun.Shotgun(game.world_engine, game.physics_engine, game.physics_engine.player.get_pos())
    game.physics_engine.player.inventory.add_item(shotgun)
    
    from enemy_models import Mothership
    mothership = Mothership.Mothership(game.world_engine, game.physics_engine, (300,300))
    game.physics_engine.add_enemie(mothership)

    # def test(wordlengine_ref:world.WorldEngine, physicsengine_ref:physics.Physics, **kwargs):
    #     # physicsengine_ref.player.health.take_damage(1)
    #     physicsengine_ref.player.set_pos(settings.player_starting_pos)
    #     print("test")
        
    # def test2(wordlengine_ref:world.WorldEngine, physicsengine_ref:physics.Physics, tick_lenght:float, **kwargs):
    #     physicsengine_ref.player.health.take_damage(10*tick_lenght)

    # zone = physics.Triggerzone(game.world_engine, game.physics_engine, (600,800), (100,100), test)
    # zone2 = physics.Triggerzone(game.world_engine, game.physics_engine, (550,800), (100,200), test2)
    # game.physics_engine.trigger_zones.append(zone)
    # game.physics_engine.trigger_zones.append(zone2)
    
    game.run()
 

if __name__ == "__main__":
    # cProfile.run('play_mode()', sort='tottime')
    play_mode()
