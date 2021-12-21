import spot

from core.specification.sformula import Sformula


def spot_example():
    """Spot Simplify is not good for booleans."""
    f = spot.formula("!b & (a | b)")
    f.simplify()
    print(f)


def example_1():
    phi = "! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)"
    sformula = Sformula(phi)
    print(sformula.represent())


def example_boolean_ops():
    # f1 = Sformula("a | b")
    # f2 = Sformula("c & b")
    # phi = f1 & f2
    # print(phi.represent())
    #
    # phi = f1 | f2
    # print(phi.represent())

    c = Sformula("c")
    g = ~c
    print(g.represent())

    # phi = f1 >> f2
    # print(phi.represent())


if __name__ == "__main__":
    example_boolean_ops()
