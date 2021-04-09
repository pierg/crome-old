from worlds import World
from worlds.crome.types.locations import *
from worlds.crome.types.sensors import *
from worlds.crome.types.actions import *
from worlds.crome.types.context import *


class Crome(World):

    def __init__(self):
        super().__init__({
            Person(),
            R1(),
            R2(),
            R3(),
            R4(),
            R5(),
            Day(),
            Night(),
            Severe(),
            Greet(),
            Cure()
        })
