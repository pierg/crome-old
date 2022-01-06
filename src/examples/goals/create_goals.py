from core.cgg import Node
from core.patterns.robotics.coremovement.surveillance import StrictOrderedPatrolling
from core.patterns.robotics.trigger import BoundReaction
from core.specification import SpecNotSATException
from core.specification.lformula import LTL
from examples.types.create_world import ExampleWorld

"""We import the world"""
w = ExampleWorld()


def test1():
    n1 = (
        Node(
            name="day_patrol_12",
            description="During context day => start from r1, patrol r1, r2 in strict order,\n"
            "Strict Ordered Patrolling Location r1, r2",
            context=w["day"],
            specification=LTL(StrictOrderedPatrolling("r1", "r2")),
            world=w,
        ),
    )

    print(n1)


def build_set_of_goals():
    """Spot Simplify is not good for booleans."""
    """Modeling the set of goals using robotic robotic.json."""
    set_of_goals = {
        Node(
            name="day_patrol_12",
            description="During context day => start from r1, patrol r1, r2 in strict order,\n"
            "Strict Ordered Patrolling Location r1, r2",
            context=w["day"],
            specification=LTL(StrictOrderedPatrolling("r1", "r2")),
            world=w,
        ),
        Node(
            name="night_patrol_34",
            description="During context night => start from r3, patrol r3, r4 in strict order,\n"
            "Strict Ordered Patrolling Location r3, r4",
            context=w["night"],
            specification=LTL(StrictOrderedPatrolling("w3", "w4")),
            world=w,
        ),
        Node(
            name="greet_person",
            description="Always => if see a person, greet in the same step,\n"
            "Only if see a person, greet immediately",
            specification=BoundReaction(w["person"], w["greet"]),
            world=w,
        ),
        Node(
            name="register_person",
            description="During context day => if see a person, register in the next step,\n"
            "Only if see a person, register in the next step",
            context=w["day"],
            specification=BoundDelay(w["person"], w["register"]),
            world=w,
        ),
    }

    return set_of_goals


def example_1():
    phi = "! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)"
    sformula = LTL(phi)
    print(sformula.tree(LTL.TreeType.LTL))
    print(sformula.tree(LTL.TreeType.BOOLEAN))
    print(sformula.represent(LTL.Output.SUMMARY))


def example_boolean_ops():
    f1 = LTL("a | b")
    f2 = LTL("c & b")
    phi = f1 & f2
    print(phi.represent())

    phi = f1 | f2
    print(phi.represent())

    phi = ~f2
    print(phi.represent())

    phi = ~f2 | ~f1
    print(phi.represent())

    phi = f1 >> f2
    print(phi.represent())

    f1 &= f2
    print(f1.represent())

    f2 |= f1
    print(f2.represent())


def inconsistencies():
    # f1 = LTL("G(a)")
    # f2 = LTL("!G(a)")
    # phi_2 = "(! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)) & z"
    # phi_2_ltl = LTL(phi_2)
    try:
        # phi = LTL("a & !a")
        # phi = LTL("a | !a")
        phi = LTL(
            "(! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p))"
        )
        print(phi.tree(LTL.TreeType.LTL))
        print(phi.tree(LTL.TreeType.BOOLEAN))
        print(phi.represent(LTL.Output.SUMMARY))
    except SpecNotSATException as e:
        print(f"{e.formula.original_formula} is not satisfiable")


if __name__ == "__main__":
    test1()
