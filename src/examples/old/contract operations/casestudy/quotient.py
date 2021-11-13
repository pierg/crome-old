from custom_world import CustomWorld

from core.cgg import Node
from core.specification.atom.pattern.robotics.coremovement.surveillance import *

w = CustomWorld()

patrol = Node(
    name="always_visit_r5_r4",
    description="patrolling of r5 and r4",
    specification=Patrolling([w["r5"], w["r4"]]),
    world=w,
)
"""Contract
    A: TRUE
    G: G(F(r5)) & G(F(r4))
"""

print(patrol)

print("let us now try to refine 'patrol' from 'library_1'")

library_1_goal_x = Node(
    name="always_visit_r5",
    description="patrolling of r5",
    specification=Patrolling([w["r5"]]),
    world=w,
)
print(
    "we found a goal in library 1 which has some common variables but does not refine 'patrol'"
)
assert set(library_1_goal_x.specification.typeset).intersection(
    patrol.specification.typeset
)
assert not library_1_goal_x.specification <= patrol.specification

print("let's use the 'QUOTIENT' to look at the missing part")
quotient_patrol = patrol.quotient(library_1_goal_x)
print(quotient_patrol)

print("let's look for something that refine the quotient in another library")

library_2_goal_y = Node(
    name="always_visit_r4",
    description="patrolling of r4",
    specification=Patrolling([w["r4"]]),
    world=w,
)

print("we found a goal in library_2 which refine the quotient")
assert library_2_goal_y.specification <= quotient_patrol.specification

print("let's compute the composition among the two library goals")
composition = Node.composition({library_1_goal_x, library_2_goal_y})
print(composition)

print("now we have a goal that refine patrol")
assert composition.specification <= patrol.specification
