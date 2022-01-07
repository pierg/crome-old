from core.cgg import Node
from core.patterns.robotics.coremovement.surveillance import StrictOrderedPatrolling
from core.patterns.robotics.trigger import BoundDelay, BoundReaction
from core.specification.lformula import LTL
from examples.types.create_world import ExampleWorld

"""We import the world"""
w = ExampleWorld()


set_of_goals = {
    Node(
        name="day_patrol_12",
        description="During context day => start from r1, patrol r1, r2 in strict order,\n"
        "Strict Ordered Patrolling Location r1, r2",
        context=w["dy"],
        specification=LTL(StrictOrderedPatrolling("r1", "r2"), w.typeset),
        world=w,
    ),
    Node(
        name="night_patrol_34",
        description="During context night => start from r3, patrol r3, r4 in strict order,\n"
        "Strict Ordered Patrolling Location r3, r4",
        context=w["nt"],
        specification=LTL(StrictOrderedPatrolling("w3", "w4"), w.typeset),
        world=w,
    ),
    Node(
        name="greet_person",
        description="Always => if see a person, greet in the same step,\n"
        "Only if see a person, greet immediately",
        specification=LTL(BoundReaction("ps", "gr"), w.typeset),
        world=w,
    ),
    Node(
        name="register_person",
        description="During context day => if see a person, register in the next step,\n"
        "Only if see a person, register in the next step",
        context=w["dy"],
        specification=LTL(BoundDelay("ps", "re"), w.typeset),
        world=w,
    ),
}


def one_goal():
    print("wait")

    n1 = Node(
        name="day_patrol_12",
        description="During context day => start from r1, patrol r1, r2 in strict order,\n"
        "Strict Ordered Patrolling Location r1, r2",
        context=w["dy"],
        specification=LTL(StrictOrderedPatrolling("r1", "r2"), w.typeset),
        world=w,
    )

    print(n1)


def build_set_of_goals():
    """Spot Simplify is not good for booleans."""
    """Modeling the set of goals using robotic robotic.json."""

    for g in set_of_goals:
        print(g)


if __name__ == "__main__":
    one_goal()
    build_set_of_goals()
