from physics import Enemy
import assets

class Ball(Enemy):
    image = assets.enemies['ball']
    movement_speed = 100
    size = image.get_size()
    gravity = False
    
    def __init__(self, wordlengine_ref, physicsengine_ref, pos: tuple) -> None:

        super().__init__(wordlengine_ref, physicsengine_ref, pos, self.size, self.image)