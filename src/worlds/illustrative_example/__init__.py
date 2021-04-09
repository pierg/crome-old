from worlds import World
from worlds.illustrative_example.types.locations import *
from worlds.illustrative_example.types.sensors import *
from worlds.illustrative_example.types.actions import *
from worlds.illustrative_example.types.context import *


class IllustrativeExample(World):

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
            Greet()
        })
