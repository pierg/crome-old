from worlds import World
from worlds.case_study.types.locations import *
from worlds.case_study.types.sensors import *
from worlds.case_study.types.actions import *
from worlds.case_study.types.context import *


class CaseStudy(World):

    def __init__(self):
        super().__init__({
            L1(),
            L2(),
            L3(),
            L4(),
            L5(),
            L6(),
            B1(),
            B2(),
            B3(),
            H1(),
            H2(),
            E1(),
            E2(),
            K1(),
            K2(),
            K3(),
            R1(),
            R2(),
            ObjectRecognized(),
            ObjectUnknown(),
            HoldObject(),
            DropObject(),
            PickupObject()
        })
