from custom_world import CustomWorld

from core.cgg import Node
from core.specification.atom.pattern.robotics.coremovement.surveillance import *

w = CustomWorld()

original = Node(
    name="strict_patrolling",
    description="strict order patrolling regions r1 -> r2",
    specification=StrictOrderedPatrolling([w["r1"], w["r2"], w["r5"]]),
    world=w,
)
"""Contract
    A: TRUE
    G: G(F(r1 & F(r2))) & (!(r2) U r1) & G(((r2) -> (X((!(r2) U r1))))) & G(((r1) -> (X((!(r1) U r2)))))
"""

print(original)

print("let us now try to refine 'original' from 'library_1'")

g1 = Node(
    name="library_1_goal_x",
    description="strict order patrolling regions r1 -> r2",
    specification=Patrolling([w["r1"], w["r2"]]),
    world=w,
)

g2 = Node(
    name="library_1_goal_y",
    description="strict order patrolling regions r1 -> r2",
    specification=Patrolling([w["r5"]]),
    world=w,
)

g3 = Node(
    name="library_1_goal_z",
    description="strict order patrolling regions r1 -> r2",
    specification=OrderedPatrolling([w["r2"], w["r5"]]),
    world=w,
)


g1g2 = Node.composition({g1, g2})

print(g1g2.specification <= g1.specification)
print(g1g2.specification <= g2.specification)
