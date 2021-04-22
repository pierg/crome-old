from cgg import Node
from cgg.exceptions import CGGException
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers_modified import *
from tools.persistence import Persistence
from worlds.illustrative_example import RunningExample

folder_name = "running_example"

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet in the next step
"""

"""We import the world"""
w = RunningExample()

"""Strict Ordered Patrolling Location r1, r2"""
ordered_patrol_day = StrictOrderedPatrolling([w["r1"], w["r2"]])

"""Strict Ordered Patrolling Location r3, r4"""
ordered_patrol_night = StrictOrderedPatrolling([w["r3"], w["r4"]])

"""Only if see a person, greet immediatly"""
greet = BoundReaction(w["person"], w["greet"], active=w["active"])

"""Only if see a person, register in the next step"""
register = BoundDelay(w["person"], w["register"], active=w["active"], context=w["day"])

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

    n_register = Node(name="register_person",
                      context=w["day"],
                      specification=register,
                      world=w)

    cgg = Node.build_cgg({n_day, n_night, n_greet, n_register})
    cgg.set_session_name(folder_name)
    cgg.save()
    Persistence.dump_cgg(cgg)
    print(cgg)


except CGGException as e:
    raise e
