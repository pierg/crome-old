from core.specification.atom.patterns.basic import F, G, X
from examples.types.create_types import GenericWorld

q = GenericWorld()


def g_and():
    phi = G(q["a"] & q["b"])
    phi_eq = G(q["a"]) & G(q["b"])
    phi_ab_1 = G(q["a"])
    phi_ab_2 = G(q["b"])
    assert phi == phi_eq
    assert phi_ab_1 >= phi_eq
    assert phi_ab_2 >= phi_eq


def f_or():
    phi = F(q["a"] | q["b"])
    phi_2 = F(q["a"]) | F(q["b"])
    assert phi == phi_2


def x_and():
    phi = X(q["a"] & q["b"])
    phi_2 = X(q["a"]) & X(q["b"])
    assert phi == phi_2


def x_or():
    phi = X(q["a"] | q["b"])
    phi_2 = X(q["a"]) | X(q["b"])
    assert phi == phi_2


if __name__ == "__main__":
    g_and()
    f_or()
