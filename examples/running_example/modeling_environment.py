from world import World
from running_example.variables import *


class RunningExample(World):

    def __init__(self):
        super().__init__(
            actions={
                Greet(),
                Register()
            },
            locations={
                R1(),
                R2(),
                R3(),
                R4(),
                R5(),
            },
            sensors={
                Person(),
            },
            contexts={
                Day(),
                Night()
            })
