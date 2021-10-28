from .variables import *
from core.world import World


class CustomWorld(World):

    def __init__(self):
        super().__init__(
            actions={
                Greet(),
                Register(),
                Picture()
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
                Movement()
            },
            contexts={
                Day(),
                Night()
            })
