from contract import Contract
from cgg import Node
from cgg.exceptions import CGGException
from specification.atom.pattern.robotics.coremovement.surveillance import *
from type.subtypes.context import ContextBooleanTime
from type.subtypes.locations import ReachLocation
from typeset import Typeset
from worlds import World

"""Continuation of 5_modelling_problems:
GOAL to model:
while 'day' is true => continuously visit the office, 
and while 'night' is true => continuously visit the bed
"""

"""Let us define 'day' and 'night' as Context instead"""


class Day(ContextBooleanTime):

    def __init__(self, name: str = "day"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


class Night(ContextBooleanTime):

    def __init__(self, name: str = "night"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


"""Our goals as before, using the Patrolling Pattern"""


class A1(ReachLocation):

    def __init__(self, name: str = "a1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A2", "Z"}


class A2(ReachLocation):

    def __init__(self, name: str = "a2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A1", "A"}


class B1(ReachLocation):

    def __init__(self, name: str = "b1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B2", "Z"}


class B2(ReachLocation):

    def __init__(self, name: str = "b2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B1", "Z"}


class Z(ReachLocation):

    def __init__(self, name: str = "z"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A1", "A2", "B1", "B2"}


day = Day().to_atom()
night = Night().to_atom()
a1 = A1().to_atom()
a2 = A2().to_atom()
b1 = B1().to_atom()
b2 = B2().to_atom()
z = Z().to_atom()

"""Ordered Patrolling Location a1, a2 starting from a1"""
patrol_a = a1 & OrderedPatrolling([a1, a2])

"""Ordered Patrolling Location b1, b2"""
patrol_b = b1 & OrderedPatrolling([b1, b2])

"""Inputs and Outputs"""
i_set, o_set = (patrol_a.typeset | patrol_b.typeset | z.typeset).extract_inputs_outputs()
i_typeset = Typeset(i_set)
o_typeset = Typeset(o_set)

"""Mutex"""
mutex_context = Atom.extract_mutex_rules(i_typeset)
mutex_locs = Atom.extract_mutex_rules(o_typeset)

"""Liveness"""
live_day = Atom.extract_liveness_rules(day.typeset)
live_night = Atom.extract_liveness_rules(night.typeset)

"""Topology"""
topology = Atom.extract_adjacency_rules(o_typeset)

c1 = Contract(assumptions=live_day, guarantees=patrol_a & mutex_locs & topology)
c2 = Contract(assumptions=live_night, guarantees=patrol_b & mutex_locs & topology)

print(c1)
print(c2)

# c = Contract(assumptions=c1.assumptions & c2.assumptions, guarantees=c1.guarantees | c2.guarantees)
c = Contract.disjunction({c1, c2})

print(c)
print(c1 <= c)
print(c2 <= c)
