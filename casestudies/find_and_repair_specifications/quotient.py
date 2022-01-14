from casestudies.find_and_repair_specifications.goals import w
from core.cgg import Node
from core.contract import Contract
from core.patterns.robotics.coremovement.coverage import OrderedVisit
from core.patterns.robotics.coremovement.surveillance import (
    OrderedPatrolling,
    Patrolling,
)
from core.specification.lformula import LTL

g_prime = Node(
    name="night_patrolling",
    description="During the night patrol in order all the locations in a strict order",
    context=w["nt"],
    specification=Contract(
        assumptions=None,
        guarantees=LTL(OrderedPatrolling("l1", "l3", "l5"), w.typeset),
    ),
    world=w,
)

l1 = Node(
    name="patrol_l1_l2",
    description="Keep visiting l1 and l2",
    specification=LTL(Patrolling("l1", "l5"), w.typeset),
    world=w,
)

l2 = Node(
    name="patrol_l3",
    description="Keep visiting l3",
    specification=LTL(Patrolling("l3"), w.typeset),
    world=w,
)

candidate_composition = Node.composition({l1, l2})

print(f"The composition is: \n'{candidate_composition}'")

if not candidate_composition <= g_prime:
    print("The candidate_composition does not refine g_prime")

quotient = candidate_composition.quotient(g_prime)
print(f"The quotient is: \n'{quotient}'")

print(quotient.specification.assumptions.spot_formula._repr_latex_())
print(quotient.specification.guarantees.spot_formula._repr_latex_())


l_prime_1 = Node(
    name="strict_order_visit_locations",
    description="l1 -> l3 -> l5 -> l4 -> l2",
    specification=LTL(OrderedVisit("l1", "l3", "l5", "l4", "l2"), w.typeset),
    world=w,
)

if l_prime_1 <= quotient:
    print("The library goal l_prime_1 refines the quotient")

composition = Node.composition({l_prime_1, candidate_composition})
print(f"The composition of l_prime_1 with candidate_composition is: \n'{composition}'")

if composition <= quotient:
    print("The composition now refines the initial goal g_prime")
