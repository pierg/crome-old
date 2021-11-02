from core.cgg import Node
from core.specification.atom.pattern.robotics.coremovement.surveillance import *
from custom_world import CustomWorld

w = CustomWorld()

strict_order = Node(name="strict_patrolling",
                    description="strict order patrolling regions r1 -> r2",
                    specification=StrictOrderedPatrolling([w["r1"], w["r2"], w["r5"]]),
                    world=w)
"""Contract
    A: TRUE
    G: G(F(r1 & F(r2))) & (!(r2) U r1) & G(((r2) -> (X((!(r2) U r1))))) & G(((r1) -> (X((!(r1) U r2))))) 
"""

print(strict_order)

print("let us now try to refine 'strict_order' from 'library_1'")

g1 = Node(name="library_1_goal_z",
          description="strict order patrolling regions r1 -> r2",
          specification=Patrolling([w["r1"], w["r2"]]),
          world=w)

g2 = Node(name="library_1_goal_z",
          description="strict order patrolling regions r1 -> r2",
          specification=Patrolling([w["r5"]]),
          world=w)

g3 = Node(name="library_1_goal_z",
          description="strict order patrolling regions r1 -> r2",
          specification=OrderedPatrolling([w["r2"], w["r5"]]),
          world=w)

library_1_goal_z = Node.composition({g1, g2, g3})

print("we found a goal in library 1 which has some common variables but does not refine 'strict_patrolling'")
assert set(library_1_goal_z.specification.typeset).intersection(strict_order.specification.typeset)
assert not library_1_goal_z.specification <= strict_order.specification

print("let's use the 'QUOTIENT' to look at the missing part")
quotient_strict_order = strict_order.quotient(library_1_goal_z)
print(quotient_strict_order)

print("let's look for something that refine the quotient in another library")
print("unfortunately we could not find anything that refine the quotient")
print("let's compute the separation on what we have a find the smallest change we have to add to our specification "
      "so that the goal we have is enough to refine")

separation = library_1_goal_z.separation(strict_order)
print(separation)

print("now we can merge what we found with our original goal")
merger = Node.merging({strict_order, separation})
print(merger)
print("our library goal now refines the merged specification")
assert library_1_goal_z.specification <= merger.specification

print("thanks to the separation and the merging the initial specification has been 'relaxed' "
      "to accommodate what is available in the library")
assert strict_order.specification <= merger.specification
