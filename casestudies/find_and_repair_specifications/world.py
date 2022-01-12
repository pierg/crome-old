from casestudies.find_and_repair_specifications.ctypes import (
    L1,
    L2,
    L3,
    L4,
    L5,
    Back,
    Charge,
    Charging,
    Day,
    Front,
    Night,
    Person,
    Picture,
    Report,
    Wave,
)
from core.world import World


class StoreWorld(World):
    def __init__(self):
        super().__init__(
            actions={Picture(), Charge(), Report(), Wave()},
            locations={Front(), Back(), Charging(), L1(), L2(), L3(), L4(), L5()},
            sensors={Person()},
            contexts={Day(), Night()},
        )
