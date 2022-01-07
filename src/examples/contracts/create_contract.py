from core.contract import Contract
from core.specification import SpecNotSATException
from core.specification.lformula import LTL
from examples.types.create_world import ExampleWorld

"""We import the world"""
w = ExampleWorld()


def create_contract():
    c = Contract(
        assumptions=LTL("night", w.typeset), guarantees=LTL("F day", w.typeset)
    )

    print(c)

    print("\n\n")

    try:
        c = Contract(
            assumptions=LTL("night", w.typeset), guarantees=LTL("!night", w.typeset)
        )
    except SpecNotSATException:
        print("Spec non satisfiable")

    print("\n\n")

    try:
        c = Contract(
            assumptions=LTL("G(a & b) | F(c & k)"), guarantees=LTL("G(!a) & G(!c)")
        )
    except SpecNotSATException:
        print("Spec non satisfiable")


if __name__ == "__main__":
    create_contract()
