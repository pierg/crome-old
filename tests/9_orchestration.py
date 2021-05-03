from cgg import Node
from cgg.exceptions import CGGException
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import BoundDelay
from tools.persistence import Persistence
from examples.running_example.world import RunningExample

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet
"""

"""We import the world"""
w = RunningExample()

"""Strict Ordered Patrolling Location r1, r2"""
ordered_patrol_day = StrictOrderedPatrolling([w["r1"], w["r2"]])
print("one\n" + str(ordered_patrol_day))

"""Strict Ordered Patrolling Location r3, r4"""
ordered_patrol_night = StrictOrderedPatrolling([w["r3"], w["r4"]])
print("two\n" + str(ordered_patrol_night))

"""Only if see a person, greet in the next step"""
greet = BoundDelay(w["person"], w["greet"])

try:

    n_day = Node(name="day_patrol_a",
                 context=w["day"],
                 specification=ordered_patrol_day,
                 world=w)

    n_night = Node(name="night_patrol_b",
                   context=w["night"],
                   specification=ordered_patrol_night,
                   world=w)

    n_greet = Node(name="greet_person",
                   specification=greet,
                   world=w)

    cgg = Node.build_cgg({n_day, n_night, n_greet})
    cgg.session_name = "running_example_delayed"
    cgg.save()
    cgg.realize_all(t_trans=3)
    Persistence.dump_cgg(cgg)
    print(cgg)




except CGGException as e:
    raise e
