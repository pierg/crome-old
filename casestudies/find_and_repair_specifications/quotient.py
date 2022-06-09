from casestudies.find_and_repair_specifications.goals import w
from core.cgg import Node
from core.contract import Contract
from core.library import Library
from core.patterns.robotics.coremovement.coverage import Visit
from core.patterns.robotics.coremovement.surveillance import (
    OrderedLocations,
    OrderedPatrolling,
    Patrolling,
    StrictOrderLocations,
)
from core.specification.lformula import LTL
from tools.strings import StringMng


print(OrderedLocations("l1", "l3"))
print(OrderedLocations("l3", "l5"))
print(OrderedLocations("l1", "l3", "l5"))


goal_to_refine = Node(
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


lib1_goals = {
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
        name="l4",
        description="Keep visiting l3",
        specification=LTL(Visit("l5"), w.typeset),
        world=w,
    ),
}

library = Library(lib1_goals)

candidate_composition = library.get_candidate_composition(goal_to_refine=goal_to_refine)

print(candidate_composition)

print(f"The candidate composition is: \n'{candidate_composition}'")

if not candidate_composition <= goal_to_refine:
    print("The candidate_composition does not refine g_prime")

quotient = Node.quotient(dividend=goal_to_refine, divisor=candidate_composition)
print(f"The quotient is: \n'{quotient}'")
print(StringMng.latexit(quotient.specification.assumptions))
print(StringMng.latexit(quotient.specification.guarantees))


#
# lib_2_goals = {
#     Node(
#         name="order_3",
#         description="l5 -> l1 -> l3",
#         specification=LTL(OrderedLocations("l1", "l3", "l5"), w.typeset),
#         world=w,
#     ),
# }
#
# print(StringMng.latexit(list(lib_2_goals)[0].specification.guarantees))
#
#
# library_2 = Library(lib_2_goals)
#
# l_prime_1 = library_2.search_refinement(quotient)
# if l_prime_1 <= quotient:
#     print(f"The library goal {l_prime_1} refines the quotient")


l_prime_1 = Node(
    name="order_3",
    description="l5 -> l1 -> l3",
    specification=LTL(StrictOrderLocations("l1", "l3", "l5"), w.typeset),
    world=w,
)

if l_prime_1 <= quotient:
    print(f"The library goal {l_prime_1} refines the quotient")

print(StringMng.latexit(l_prime_1.specification.guarantees))


composition = Node.composition({l_prime_1, candidate_composition})
print(
    f"The composition of {l_prime_1.name} with candidate_composition is: \n'{composition}'"
)

if composition <= goal_to_refine:
    print("The composition now refines the initial goal g_prime")
