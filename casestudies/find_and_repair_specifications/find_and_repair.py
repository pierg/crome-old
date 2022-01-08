from casestudies.find_and_repair_specifications.cgg import cgg
from casestudies.find_and_repair_specifications.goals import w
from core.cgg import Node
from core.goal import Goal
from core.library import Library
from core.patterns.robotics.coremovement.surveillance import Patrolling
from core.specification.lformula import LTL

library_goals = {
    Goal(
        name="patrol_l1_l2",
        description="Keep visiting l1 and l2",
        specification=LTL(Patrolling("l1", "l2"), w.typeset),
        world=w,
    ),
    Goal(
        name="patrol_l1_l2_l3_l4",
        description="Keep visiting l1 and l2",
        specification=LTL(Patrolling("l1", "l2", "l3", "l4"), w.typeset),
        world=w,
    ),
}

g1 = Goal(
    name="patrol_l1_l2",
    description="Keep visiting l1 and l2",
    specification=LTL(Patrolling("l1", "l2"), w.typeset),
    world=w,
)

n1 = Node(
    name="day_visit",
    description="During the day keep visiting the front of the store",
    context=w["dy"],
    specification=LTL(Patrolling("ft"), w.typeset),
    world=w,
)

print(g1 <= n1)
print("wewe")


library = Library(library_goals)

leaves = cgg.get_leaves()

for goal in leaves:
    refinement = library.search_refinement(goal)
    if refinement is not None:
        print(f"{refinement.name}\trefines\t{goal.name}")

print(leaves)
print(leaves)
