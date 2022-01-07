from casestudies.find_and_repair_specifications.ctypes import (
    L1,
    L2,
    L3,
    L4,
    L5,
    Back,
    Day,
    Front,
    Greet,
    Movement,
    Night,
    Person,
    Picture,
    Report,
)
from core.world import World


class StoreWorld(World):
    def __init__(self):
        super().__init__(
            actions={Picture(), Greet(), Report()},
            locations={Front(), Back(), L1(), L2(), L3(), L4(), L5()},
            sensors={Movement(), Person()},
            contexts={Day(), Night()},
        )
