from typing import Tuple
import numpy as np
import logging
from pathlib import Path
import os


class World():
    def __init__(self, worldName) -> None:
        self.worldName = worldName
    
        self.logger = logging.getLogger("worldEngine.worldHandler")
        logging.basicConfig(level=logging.DEBUG, filename="GameLog.log", format="%(asctime)s - %(levelname)-8s - %(name)-25s - %(message)s")

        self.loadWorld()

    def saveWorld(self):
        writeNumpyWorldToMemory(self.world, self.worldName)
        self.logger.info(f"saved World: {self.worldName}")

    def loadWorld(self):
        self.world = loadNumpyWoldFromMemory(self.worldName)
        self.logger.info(f"loaded world: {self.worldName}")

    def getBlock(self, blockposition: tuple [int, int]) -> int:
        block = self.world[blockposition[0]][blockposition[1]]
        return block

    def changeBlock(self, blockposition: Tuple[int, int], resultBlock: int):
        try:
            self.world[blockposition[0]][blockposition[1]] = resultBlock
            self.logger.debug(f"changed Block at {blockposition[0]} | {blockposition[1]} to {resultBlock}")
        except Exception:
            print(f"blcok out of range | {blockposition}")
            print(Exception)


def setBlockInWorld(world: np.array, BlockPos: Tuple[int, int], BlockValue: int):
    world[BlockPos[0]][BlockPos[1]] = BlockValue
    return world

def getBlockInWorld(world: np.array, BlockPos: Tuple[int, int]):
    return world[BlockPos[0]][BlockPos[1]]

def getNewNumpyWorld(width: int, height: int):
    world = np.zeros((width, height), dtype=np.int8)
    return world

def writeNumpyWorldToMemory(world: np.array, location: str):
    dictPath = Path(__file__)
    dictPath = os.path.dirname(dictPath)
    np.save(f"{dictPath}/worlds/{location}.npy", world)

def loadNumpyWoldFromMemory(location: str):
    dictPath = Path(__file__)
    dictPath = os.path.dirname(dictPath)
    world = np.load(f"{dictPath}/worlds/{location}.npy")
    return world

def giveWorldFloor(world: np.array, floorHeight: int, Blockvalue: int):
    for xIndex, x in enumerate(world):
        for yIndex, y in enumerate(x):
            if yIndex == floorHeight:
                world[xIndex][yIndex] = Blockvalue
    return world

def printWorld(world: np.array):
    for line in world:
        print(line)

if __name__ == "__main__":
    newWorld = getNewNumpyWorld(300, 300)
    newWorld = giveWorldFloor(newWorld, 10, 3)
    print(newWorld)
    printWorld(newWorld)
    writeNumpyWorldToMemory(newWorld, "testWorldAllZero")
    # world = World("test.txt")
    # print(world.world, "\n")
    # world.saveWorld()
    # world.loadWorld()
    # print(world.world)