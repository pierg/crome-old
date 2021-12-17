from core.specification.atom.patterns.basic import GF, F, G, U, X
from core.specification.formula import Formula
from examples.types.create_types import GenericWorld
from examples.types.create_world import ExampleWorld

"""Import Our World"""
w = ExampleWorld()

q = GenericWorld()

"""Our goal is to create a 'Specification' class, i.e. a 'Formula' using
    'Atoms'."""

"""Specification to create:
        atoms:  r1, r2, r3, r4, pc, gr, pc, re
        LTL:    (GF(r1) & GF(r2)) | (GF(r3) & GF(r4))) & G(pc -> gr) & F(pc -> X re)  & (r1 U r2)
"""


def method_1():
    """METHOD 1: Use Temporal Operators Library on Atoms."""

    """we can split the specification if blocks"""
    a = GF(w["r1"]) & GF(w["r2"])
    b = GF(w["r3"]) & GF(w["r4"])
    c = G(w["pc"] >> w["gr"])
    d = F(w["pc"] >> X(w["gr"]))
    e = U(w["r1"], w["r2"])
    phi = (a | b) & c & d & e

    return phi


def method_2():
    """Parse formula using SPOT."""
    phi_string = "((!GF(r1) & GF(r2)) | (GF(r3) & GF(r4))) & G(pc -> gr) & F(pc -> X re)  & (r1 U r2)"
    # phi_string = "!((GF(r1) & GF(r2)) -> (F(pc -> gr) & G(pc -> gr)) ) | (G(r1 U r2) & X(r1 U r2))"
    # phi_string = "G(pc & gr) | G(pc -> re)"
    phi = Formula(phi_string, world=w)


if __name__ == "__main__":
    # phi_1 = method_1()
    phi_2 = method_2()
