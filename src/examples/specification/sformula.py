import spot

from core.specification.lformula import LTL


def spot_example():
    """Spot Simplify is not good for booleans."""
    f = spot.formula("!b & (a | b)")
    f.simplify()
    print(f)


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
    phi = LTL("a | !a")
    print(phi.tree(LTL.TreeType.LTL))
    print(phi.tree(LTL.TreeType.BOOLEAN))
    print(phi.represent(LTL.Output.SUMMARY))


if __name__ == "__main__":
    inconsistencies()
