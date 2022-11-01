from typing import Tuple
import numpy as np
import settings

class WorldEngine:
    def __init__(self) -> None:
        self.world_name = settings.world_name
        self.set_new_world(settings.world_dimensions)

    def set_new_world(self, dimensions:Tuple[int, int]):
        self.world = np.zeros((dimensions[0], dimensions[1]), dtype=np.int8)

    def load_world_from_memory(self):
        self.world = np.load(f"{settings.dictPath}/worlds/{self.world_name}.npy")

    def save_world_to_memory(self):
        np.save(f"{settings.dictPath}/worlds/{self.world_name}.npy", self.world)       


if __name__ == "__main__":
    world_engine = WorldEngine()
    world_engine.save_world_to_memory()