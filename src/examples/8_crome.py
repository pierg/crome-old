from core.cgg import Node
from core.cgg.exceptions import CGGException
from core.specification.atom.pattern.robotics.coremovement.surveillance import *
from core.specification.atom.pattern.robotics.trigger.triggers import InstantaneousReaction, BoundDelay
from core.world.crome import Crome

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet
"""

"""We import the variables"""
w = Crome()

"""Strict Ordered Patrolling Location r1, r2"""
ordered_patrol_day = StrictOrderedPatrolling([w["r1"], w["r2"]])
print("one\n" + str(ordered_patrol_day))

"""Strict Ordered Patrolling Location r3, r4"""
ordered_patrol_night = StrictOrderedPatrolling([w["r3"], w["r4"]])
print("two\n" + str(ordered_patrol_night))

"""Only if see a person, greet in the next step"""
greet = BoundDelay(w["person"], w["greet"])

"""Only if see a person, greet in the next step"""
cure = InstantaneousReaction(w["person"], w["cure"])

try:

    n_day = Node(name="day_patrol_a",
                 context=w["day"],
                 specification=ordered_patrol_day,
                 world=w)

    n_night = Node(name="night_patrol_b",
                   context=w["night"],
                   specification=ordered_patrol_night,
                   world=w)

    n_cure = Node(name="cure",
                  context=w["severe"],
                  specification=cure,
                  world=w)

    n_greet = Node(name="greet_person",
                   specification=greet,
                   world=w)

    cgg = Node.build_cgg({n_day, n_night, n_greet, n_cure})
    print(cgg)



except CGGException as e:
    raise e