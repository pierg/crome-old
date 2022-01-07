from core.contract import Contract
from core.specification.lformula import LTL
from examples.types.create_types import GenericWorld

"""We import the world"""
w = GenericWorld()


def composition1():
    c2 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    c1 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    c = Contract.composition({c1, c2})

    print(c)


def composition2():
    c2 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    print(c2)

    c1 = Contract(assumptions=LTL("c", w.typeset), guarantees=LTL("d", w.typeset))

    print(c1)

    c = Contract.composition({c1, c2})

    print(c)


def composition3():
    """TODO: check why 'b' is not simplified from the assumptions"""
    c2 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    print(c2)

    c1 = Contract(assumptions=LTL("b", w.typeset), guarantees=LTL("c", w.typeset))

    print(c1)

    c = Contract.composition({c1, c2})

    print(c)


def conjunction1():
    c2 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    c1 = Contract(assumptions=LTL("c", w.typeset), guarantees=LTL("d", w.typeset))

    c = Contract.conjunction({c1, c2})

    print(c)


def refinement():
    c2 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    c1 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b & c", w.typeset))

    print(c1 <= c2)


def merging():
    c2 = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    c1 = Contract(assumptions=LTL("c", w.typeset), guarantees=LTL("d", w.typeset))

    c = Contract.merging({c1, c2})

    print(c)


def quotient():
    top = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))

    lib = Contract(assumptions=LTL("c | a", w.typeset), guarantees=LTL("d", w.typeset))

    missing = Contract.quotient(top, lib)

    print(missing)

    assert Contract.composition({missing, lib}) <= top


def separation():
    top = Contract(assumptions=LTL("a", w.typeset), guarantees=LTL("b", w.typeset))
    print(top)

    lib = Contract(assumptions=LTL("c | a", w.typeset), guarantees=LTL("d", w.typeset))

    print(lib)

    print(lib <= top)

    merger = Contract.separation(lib, top)

    print(merger)

    assert lib <= Contract.merging({merger, top})


if __name__ == "__main__":
    composition1()
    # composition2()
    # composition3()
    # refinement()
    # merging()
    # quotient()
    # separation()
