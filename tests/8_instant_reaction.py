from cgg import Node, Link
from cgg.exceptions import CGGException
from specification import FormulaOutput
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import InstantaneousReaction, BoundReaction, Wait, \
    GlobalAvoidance, BoundDelay
from worlds.crome import Crome
from worlds.illustrative_example import IllustrativeExample

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet
"""

"""We import the world"""
w = Crome()

"""Strict Ordered Patrolling Location r1, r2"""
ordered_patrol_day = StrictOrderedPatrolling([w["r1"], w["r2"]])
print("one\n" + str(ordered_patrol_day))

"""Strict Ordered Patrolling Location r3, r4"""
ordered_patrol_night = StrictOrderedPatrolling([w["r3"], w["r4"]])
print("two\n" + str(ordered_patrol_night))

greet = InstantaneousReaction(w["person"], w["greet"])

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

    n_greet = Node(name="greet_person",
                   context=w["day"],
                   specification=greet,
                   world=w)

    cgg_c = Node.build_cgg({n_day, n_night, n_greet}, Link.CONJUNCTION)
    cgg_c.session_name = "instant_action_under_context_conjunction"
    cgg_c.realize_specification_controllers()
    cgg_c.save()
    print(cgg_c)

    # cgg_d = Node.build_cgg({n_day, n_night, n_greet}, Link.DISJUNCTION)
    # cgg_d.session_name = "instant_action_under_context_disjunction"
    # cgg_d.realize_all()
    # cgg_d.save()
    # print(cgg_d)

    conjunction = str(cgg_c.specification.guarantees)
    conjunction = conjunction.replace("r1", "location=r1") \
        .replace("r2", "location=r2") \
        .replace("r3", "location=r3") \
        .replace("r4", "location=r4").replace("r5", "location=r5")
    print(f"--conjunction\nLTLSPEC {conjunction}")

    # disjunction = str(cgg_d.specification.guarantees.formula(FormulaOutput.DNF)[0])
    # disjunction = disjunction.replace("r1", "location=r1") \
    #     .replace("r2", "location=r2") \
    #     .replace("r3", "location=r3") \
    #     .replace("r4", "location=r4").replace("r5", "location=r5")
    # print(f"--disjunction\nLTLSPEC {disjunction}")


except CGGException as e:
    raise e
