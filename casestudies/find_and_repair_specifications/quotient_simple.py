from casestudies.find_and_repair_specifications.goals import w
from core.contract import Contract
from core.goal import Goal
from core.patterns.robotics.coremovement.coverage import OrderedVisit
from core.patterns.robotics.coremovement.surveillance import (
    OrderedPatrolling,
    Patrolling,
)
from core.specification.lformula import LTL

goal_to_refine = Goal(
    name="night_patrolling",
    description="During the night patrol in order all the locations in a strict order",
    context=w["nt"],
    specification=Contract(
        assumptions=None,
        guarantees=LTL(OrderedPatrolling("l1", "l3", "l5"), w.typeset),
    ),
    world=w,
)

print(f"goal_to_refine:\n{goal_to_refine.specification.guarantees}")

l1 = Goal(
    name="l1",
    specification=LTL(Patrolling("l1", "l5"), w.typeset),
    world=w,
)
l2 = Goal(
    name="l2",
    specification=LTL(Patrolling("l3"), w.typeset),
    world=w,
)

candidate = Goal.composition({l1, l2})
print(f"candidate:\n{candidate.specification}")

quotient = Goal.quotient(dividend=goal_to_refine, divisor=candidate)

print(f"quotient:\n{quotient.specification}")

m1 = Goal(
    name="order_2",
    description="l1 -> l3 -> l5",
    specification=LTL(OrderedVisit("l1", "l3", "l5"), w.typeset),
    world=w,
)

comp = m1
print(f"patch:\n{m1.specification}")

print(comp <= quotient)

refinement = Goal.composition({candidate, comp})

print(refinement <= goal_to_refine)
