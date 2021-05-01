
from world import World
from world.predefined.simple_gridworld.types import *


class RunningExample(World):

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
            Greet(),
            Register()
        })
