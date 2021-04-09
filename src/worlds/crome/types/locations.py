from type.subtypes.locations import *

""""
    R1      R2   
        R5
    R3      R4
"""


class R1(ReachLocation):

    def __init__(self, name: str = "r1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R2", "R5"}


class R2(ReachLocation):

    def __init__(self, name: str = "r2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R1", "A"}


class R3(ReachLocation):

    def __init__(self, name: str = "r3"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R4", "R5"}


class R4(ReachLocation):

    def __init__(self, name: str = "r4"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R3", "R5"}


class R5(ReachLocation):

    def __init__(self, name: str = "r5"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R1", "R2", "R3", "R4"}
