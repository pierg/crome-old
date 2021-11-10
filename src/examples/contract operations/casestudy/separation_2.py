from core.cgg import Node
from core.contract import Contract
from core.specification.atom.pattern.basic import GF
from core.specification.atom.pattern.robotics.coremovement.surveillance import *
from custom_world import CustomWorld

w = CustomWorld()

original = Node(name="strict_patrolling",
                description="strict order patrolling regions r1 -> r2",
                specification=Contract(
                    assumptions=GF(w["picture"]),
                    guarantees=StrictOrderedPatrolling([w["r1"], w["r2"], w["r5"]])),
                world=w)
"""Contract
    A: TRUE
    G: G(F(r1 & F(r2))) & (!(r2) U r1) & G(((r2) -> (X((!(r2) U r1))))) & G(((r1) -> (X((!(r1) U r2))))) 
"""

print(original)

print("let us now try to refine 'original' from 'library_1'")

g1 = Node(name="library_1_goal_x",
          description="strict order patrolling regions r1 -> r2",
          specification=Patrolling([w["r1"], w["r2"]]),
          world=w)

g2 = Node(name="library_1_goal_y",
          description="strict order patrolling regions r1 -> r2",
          specification=Patrolling([w["r5"]]),
          world=w)

g3 = Node(name="library_1_goal_z",
          description="strict order patrolling regions r1 -> r2",
          specification=OrderedPatrolling([w["r2"], w["r5"]]),
          world=w)

library_1_goal_xyz = Node.composition({g1, g2, g3})

print("we found a goal in library 1 which has some common variables but does not refine 'strict_patrolling'")
assert set(library_1_goal_xyz.specification.typeset).intersection(original.specification.typeset)
assert not library_1_goal_xyz.specification <= original.specification

print("let's use the 'QUOTIENT' to look at the missing part")
quotient_original = original.quotient(library_1_goal_xyz)
print(quotient_original)

print("let's look for something that refine the quotient in another library")
print("unfortunately we could not find anything that refine the quotient")
print("let's compute the separation on what we have a find the smallest change we have to add to our specification "
      "so that the goal we have is enough to refine")

separation_1 = library_1_goal_xyz.separation(original)
print(separation_1)

print("now we can merge what we found with our original goal")
merger = Node.merging({original, separation_1})
print(merger)
print("our library goal now refines the merged specification")
assert library_1_goal_xyz.specification <= merger.specification

print("thanks to the separation and the merging the initial specification has been 'relaxed' "
      "to accommodate what is available in the library")
assert original.specification <= merger.specification

print("we can go back to the original 'original' specification my separating "
      "the merger from the previous separation result")

separation_2 = merger.separation(separation_1)

print(separation_2)
print(original)
assert separation_2.specification == original.specification
