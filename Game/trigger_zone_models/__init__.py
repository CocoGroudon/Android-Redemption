import os
import sys
import settings
from .spawn_tp import Spawn_Tp
from .damage import Damage

zones = {
    "spawn_tp":Spawn_Tp,
    "damage": Damage
}


