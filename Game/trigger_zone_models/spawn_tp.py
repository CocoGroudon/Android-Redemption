import world
import physics
import settings

    # zone2 = physics.Triggerzone(game.world_engine, game.physics_engine, (550,800), (100,200), test2)

class Spawn_Tp(physics.Triggerzone):
    def __init__(self, wordlengine_ref: world.WorldEngine, physicsengine_ref: physics.Physics, pos_x: int, pos_y: int, size_x:int, size_y:int, ofsett:int) -> None:
        pos = (pos_x +settings.blocksize*ofsett, pos_y)
        super().__init__(wordlengine_ref, physicsengine_ref, pos, (size_x, size_y), self.action)
        
    def action(self, **kwargs):
        self.physicsengine.player.set_pos(settings.player_starting_pos)
        
        
        
        
# def trigger(wordlengine_ref:world.WorldEngine, physicsengine_ref:physics.Physics, **kwargs):
#     # physicsengine_ref.player.health.take_damage(1)
#     physicsengine_ref.player.set_pos(settings.player_starting_pos)
#     print("test")