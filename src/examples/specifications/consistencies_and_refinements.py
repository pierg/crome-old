from core.specification.atom.patterns.basic import GF
from core.specification.exceptions import NotSatisfiableException
from examples.types.create_world import ExampleWorld

"""Import Our World, where:
        r1 and r2 refine rt
        r3 and r4 refine rb"""
w = ExampleWorld()


def basic_refinement():
    """r1 -> rt."""
    assert w["r1"] <= w["rt"]
    # Checks weather r1 -> rt is a valid formula, that is it is equivalent to:
    assert (w["r1"] >> w["rt"]).is_valid()

    """
    GF(r1) -> GF(rt)
    """
    assert GF(w["r1"]) <= GF(w["rt"])

    """
    (GF(r1) & GF(r1)) -> GF(rt)
    """
    assert (GF(w["r1"]) & GF(w["r2"])) <= GF(w["rt"])


def inconsistent_refinement():

    assert not w["r4"] <= w["r1"]


def inconsistent_refinement_2():
    try:
        w["r4"] <= (w["r1"] & w["r3"])

    except NotSatisfiableException:
        print(
            "The right side of the implication is inconsistent, so there is nothing to compare"
        )


if __name__ == "__main__":
    basic_refinement()
