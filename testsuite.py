import timeit
import main
import physics
import settings
import assets

time_physics = True
time_renderer = True

def time_physics(trialcount:int = 100):
    game = main.Game()
    physics = game.physics_engine

    tick_time = timeit.timeit(lambda: physics.tick(), number=trialcount)

    print("Physics results:")

    print(f'{"tick time:":30} {tick_time/trialcount*1000}')
    
    print("--------")



def time_renderer(trialcount:int = 100):
    game = main.Game()
    renderer = game.render_engine

    def shoot(player, angle:float = 0):
        '''creates a new standart projectile in the given direction \n
        angle *must* be given in radiants, else everythin gets scuffed'''
        projectile = physics.Projectile_Gravity(player, angle, player.get_pos()[:], settings.projectile_speed, 10)
        player.physics_engine.projectile_group.add(projectile)
    game.physics_engine.player.inventory.add_item(physics.Item(assets.texture_item[1], shoot))
    game.physics_engine.player.inventory.add_item(physics.Item(assets.textureMap[2]))
    game.physics_engine.player.inventory.add_item(physics.Item(assets.textureMap[3]))
    game.physics_engine.player.inventory.add_item(physics.Item(assets.textureMap[127]))
    print(game.physics_engine.player.inventory.get_item_list())


    rendertime = timeit.timeit(lambda: game.draw(), number=trialcount)

    world = timeit.timeit(lambda: renderer.blit_world(), number=trialcount)
    entities = timeit.timeit(lambda: renderer.blit_entities(), number=trialcount)
    player = timeit.timeit(lambda: renderer.blit_player(), number=trialcount)
    player_inventory = timeit.timeit(lambda: renderer.blit_player_inventory(), number=trialcount)
    player_inventory_full = timeit.timeit(lambda: renderer.blit_inventory_full(), number=trialcount)
    projectiles = timeit.timeit(lambda: renderer.blit_projectiles(), number=trialcount)

    block_choices = timeit.timeit(lambda: renderer.screen.blit(renderer.block_choices_screen, settings.block_choices_screen_ofsett), number=trialcount)
    debug = timeit.timeit(lambda: [renderer.debu_menu_update(), renderer.screen.blit(renderer.debug_screen, (10,10))], number=trialcount)


    print("Render results:")

    print(f'{"rendertime:":30} {rendertime/trialcount*1000}')
    print("------------------------")
    print(f'{"world:":30} {world/trialcount*1000}')
    print(f'{"entities:":30} {entities/trialcount*1000}')
    print(f'{"player:":30} {player/trialcount*1000}')
    print(f'{"player_inventory:":30} {player_inventory/trialcount*1000}')
    print(f'{"player_inventory_full:":30} {player_inventory_full/trialcount*1000}')
    print(f'{"projectiles:":30} {projectiles/trialcount*1000}')

    print(f'{"block_choices:":30} {block_choices/trialcount*1000}')
    print(f'{"debug:":30} {debug/trialcount*1000}')
    
    print("--------")

if __name__ == "__main__":
    time_physics()
    print("")
    time_renderer()