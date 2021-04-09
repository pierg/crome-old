from typing import Set

from specification.atom.pattern.robotics.coremovement.surveillance import OrderedPatrolling, Patrolling
from type.subtypes.locations import ReachLocation

"""We define 2 mutex locations: living_room and bedroom adjacent to each other"""


class GoLiving(ReachLocation):

    def __init__(self, name: str = "living_room"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoBedroom"}

    @property
    def mutex_group(self) -> str:
        return "rooms"


class GoBedroom(ReachLocation):

    def __init__(self, name: str = "bedroom"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoLiving"}

    @property
    def mutex_group(self) -> str:
        return "rooms"


"""We define 3 mutex locations: a, b, c, d in a grid as: |a|b|c|d|, and
 where locations a,b -> living_room and b,c -> bedroom"""


class GoA(GoLiving):

    def __init__(self, name: str = "a"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoB"}

    @property
    def mutex_group(self) -> str:
        return "grid_locations"


class GoB(GoLiving):

    def __init__(self, name: str = "b"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoA", "GoC"}

    @property
    def mutex_group(self) -> str:
        return "grid_locations"


class GoC(GoBedroom):

    def __init__(self, name: str = "c"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoB", "GoD"}

    @property
    def mutex_group(self) -> str:
        return "grid_locations"


class GoD(GoBedroom):

    def __init__(self, name: str = "d"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoC"}

    @property
    def mutex_group(self) -> str:
        return "grid_locations"


"""Variable instantiation"""
living_room = GoLiving()
bedroom = GoBedroom()
a = GoA()
b = GoB()
c = GoC()
d = GoD()

"""Let us create some specifications"""
patrol_ab = OrderedPatrolling([a, b])
print(patrol_ab)
patrol_living_room = Patrolling([living_room])
print(patrol_living_room)
ref_check = patrol_ab <= patrol_living_room
print(ref_check)
