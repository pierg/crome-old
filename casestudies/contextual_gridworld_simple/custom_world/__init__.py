from core.world import World

from .variables import R1, R2, R3, R4, R5, Day, Greet, Night, Person, Register


class GridworldBasicWorld(World):
    def __init__(self):
        super().__init__(
            actions={Greet(), Register()},
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
            contexts={Day(), Night()},
        )
