from core.specification.exceptions import NotSatisfiableException
from examples.types.create_world import ExampleWorld

"""Import Our World"""
w = ExampleWorld()

if __name__ == "__main__":
    """Our goal is to create a 'Specification' class, i.e. a 'Formula' using
    'Atoms'."""

    """Specification to create:
            atoms:  r1, r2, r3, r4, pc, gr, pc, re
            LTL:    ( GF(r1) & GF(r2) | GF(r3) & GF(r4) ) & G(pc -> gr) & G(pc -> X re)
    """

    """METHOD 1: Use Temporal Operators Library on Atoms"""

    try:
        x = w["r1"] & w["r2"]
    except NotSatisfiableException:
        print("r1 and r2 are two mutually exclusive locations!")

    """METHOD 2: Use Spot to parse an LTL string"""

    try:
        x = w["pc"] & w["gr"]
        print(x)
    except NotSatisfiableException:
        print("something went wrong")
