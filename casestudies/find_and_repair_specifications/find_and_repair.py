import os

from casestudies.find_and_repair_specifications.cgg import cgg
from casestudies.find_and_repair_specifications.goals import w
from core.goal import Goal
from core.library import Library
from core.patterns.robotics.coremovement.surveillance import Patrolling
from core.specification.lformula import LTL
from tools.persistence import Persistence

output_folder_path = (
    f"{Persistence.default_folder_path}/casestudies/{os.path.basename(os.getcwd())}"
)


l1 = Goal(
    name="patrol_l1_l2",
    description="Keep visiting l1 and l2",
    specification=LTL(Patrolling("l1", "l2"), w.typeset),
    world=w,
)

l2 = Goal(
    name="patrol_l1_l2_l3_l4",
    description="Keep visiting l1 and l2",
    specification=LTL(Patrolling("l1", "l2", "l3", "l4"), w.typeset),
    world=w,
)

library_goals = {l1, l2}

library = Library(library_goals)

leaves = cgg.get_leaves()

candidate_goals = set()
for goal in leaves:
    if library.covers(goal):
        candidate_goals.add(goal)
print(
    f"Candidate goals which are covered by the library:\n{[g.name for g in list(candidate_goals)]}"
)


refined_goals = set()
for goal in leaves:
    refinement = library.search_refinement(goal)
    if refinement is not None:
        print(f"{refinement.name}\trefines\t{goal.name}")
        """We attach the refinement to the existing goal"""
        goal.refine_by(refinement)
        print(cgg)
        refined_goals.add(goal)

print(
    f"There are still {len(candidate_goals - refined_goals)} goals that are covered by the library "
    f"but are have no refinement"
)

candidate_goals = set()
for goal in leaves - refined_goals:
    if library.covers(goal):
        candidate_goals.add(goal)

print(
    f"Candidate goals which are covered by the library:\n{[g.name for g in list(candidate_goals)]}"
)
leaves_dict = cgg.get_leaves_dict()

print(f"Library goal '{l1.name}' refines CGG leaf '{leaves_dict['day_visit'].name}'")
assert l1 <= leaves_dict["day_visit"]

print(
    f"Library goal '{l2.name}' covers CGG leaf '{leaves_dict['night_patrolling'].name}'"
)
assert not l2 <= leaves_dict["night_patrolling"]


quotient = l2.quotient(leaves_dict["night_patrolling"])
print(f"The quotient is: \n'{quotient}'")

composition = Goal.composition({quotient, leaves_dict["night_patrolling"]})
print(f"Their composition is: \n'{composition}'")

assert composition <= leaves_dict["night_patrolling"]
print(
    f"Library goal '{l2.name}' composed with the quotient refines the CGG leaf '{leaves_dict['night_patrolling'].name}'"
)

print("Searching for refinements of the quotient...")
print("No refinement has been found...")

print(
    "Modifying existing goal of CGG such that the current library goal can refine it, using separation and merging"
)
