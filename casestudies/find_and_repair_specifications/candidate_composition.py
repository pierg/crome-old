from casestudies.find_and_repair_specifications.goals import w
from core.cgg import Node
from core.contract import Contract
from core.library import Library
from core.patterns.robotics.coremovement.coverage import Visit
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

set_of_goals = {
    Node(
        name="l1",
        specification=LTL(Patrolling("l1", "l5"), w.typeset),
        world=w,
    ),
    Node(
        name="l2",
        specification=LTL(Patrolling("l3"), w.typeset),
        world=w,
    ),
    Node(
        name="l3",
        specification=LTL(Visit("l3", "l1"), w.typeset),
        world=w,
    ),
    Node(
        name="4",
        description="Keep visiting l3",
        specification=LTL(Visit("l5"), w.typeset),
        world=w,
    ),
}


library = Library(set_of_goals)

candidate_composition = library.get_candidate_composition(goal_to_refine=g_prime)

print(candidate_composition)


#
#
#
# print(f"The composition is: \n'{candidate_composition}'")
#
# if not candidate_composition <= g_prime:
#     print("The candidate_composition does not refine g_prime")
#
# quotient = candidate_composition.quotient(g_prime)
# print(f"The quotient is: \n'{quotient}'")
#
# print(quotient.specification.assumptions.spot_formula._repr_latex_())
# print(quotient.specification.guarantees.spot_formula._repr_latex_())
#
# l_prime_1 = Node(
#     name="strict_order_visit_locations",
#     description="l1 -> l3 -> l5 -> l4 -> l2",
#     specification=LTL(OrderedVisit("l1", "l3", "l5", "l4", "l2"), w.typeset),
#     world=w,
# )
#
# if l_prime_1 <= quotient:
#     print("The library goal l_prime_1 refines the quotient")
#
# composition = Node.composition({l_prime_1, candidate_composition})
# print(f"The composition of l_prime_1 with candidate_composition is: \n'{composition}'")
#
# if composition <= quotient:
#     print("The composition now refines the initial goal g_prime")
