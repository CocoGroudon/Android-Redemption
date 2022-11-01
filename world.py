from typing import Tuple
import numpy as np
import settings

class WorldEngine:
    def __init__(self) -> None:
        self.world_name = settings.world_name
        self.load_world_from_memory()

    def set_new_world(self, dimensions:Tuple[int, int]) -> None:
        self.world = np.zeros((dimensions[0], dimensions[1]), dtype=np.int8)

    def load_world_from_memory(self) -> None:
        self.world = np.load(f"{settings.dictPath}/worlds/{self.world_name}.npy")

    def save_world_to_memory(self):
        np.save(f"{settings.dictPath}/worlds/{self.world_name}.npy", self.world)       

    def get_block(self, block_position:Tuple[int, int]) -> int:
        return self.world[block_position[0]][block_position[1]]

    def set_block(self, block_position:Tuple[int, int], block_value: int) -> None:
        self.world[block_position[0]][block_position[1]] = block_value


if __name__ == "__main__":
    world_engine = WorldEngine()
    world_engine.set_new_world(settings.world_dimensions)
    world_engine.set_block((5,2), 127)
    world_engine.save_world_to_memory()