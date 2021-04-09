from typing import List, Union
from specification.atom import Atom
from specification.atom.pattern.robotics.coremovement import CoreMovement
from tools.logic import Logic
from type import Boolean


class Visit(CoreMovement):
    """Given a set of locations the robot should visit all the locations."""

    def __init__(self, ls: Union[Atom, Boolean, List[Atom], List[Boolean]] = None):
        new_typeset, loc = CoreMovement.process_input(ls)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in loc:
            f.append(Logic.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        new_formula = Logic.and_(f)

        super().__init__(formula=(new_formula, new_typeset))


if __name__ == '__main__':
    op = Visit([Boolean("a"), Boolean("b"), Boolean("c")])
    print(op)
    print("ciao")
