from core.specification.legacy.atom import F, G, U, X
from core.specification.legacy.formula import Formula
from examples.types.create_types import GenericWorld

q = GenericWorld()


def g_or():
    phi = G(q["a"] | q["b"])
    phi_ab = Formula("TRUE")
    assert phi_ab >= phi


def g_u():
    phi = G(U(q["a"], q["b"]))
    phi_ab = G(q["a"] | q["b"])
    assert phi_ab == phi


def f_and():
    phi = F(q["a"] | q["b"])
    phi_2 = F(q["a"]) | F(q["b"])
    assert phi == phi_2


def f_u():
    phi = F(q["a"] | q["b"])
    phi_2 = F(q["a"]) | F(q["b"])
    assert phi == phi_2


def x_u():
    phi = X(q["a"] | q["b"])
    phi_2 = X(q["a"]) | X(q["b"])
    assert phi == phi_2


def f_or():
    phi = F(q["a"] | q["b"])
    phi_2 = F(q["a"]) | F(q["b"])
    assert phi == phi_2


def f_u():
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


def x_u():
    phi = X(q["a"] | q["b"])
    phi_2 = X(q["a"]) | X(q["b"])
    assert phi == phi_2


if __name__ == "__main__":
    g_u()
