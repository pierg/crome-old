from typing import List, Union
from specification.atom import Atom
from specification.atom.pattern.robotics.coremovement import CoreMovement
from tools.logic import Logic as L
from type import Boolean


class Visit(CoreMovement):
    """Given a set of locations the robot should visit all the locations."""

    def __init__(self, ls: Union[Atom, Boolean, List[Atom], List[Boolean]] = None):
        new_typeset, loc = CoreMovement.process_input(ls)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in loc:
            f.append(L.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        new_formula = L.and_(f)

        super().__init__(formula=(new_formula, new_typeset))



class OrderedVisit(CoreMovement):
    """Given a set of locations the robot should visit all the locations."""

    def __init__(self, ls: Union[Atom, Boolean, List[Atom], List[Boolean]] = None):
        new_typeset, loc = CoreMovement.process_input(ls)

        new_typeset, loc = CoreMovement.process_input(ls)
        lor = list(loc)
        lor.reverse()
        n = len(loc)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in loc:
            f.append(L.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        f1 = L.and_(f)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(loc[:n - 1]):
            f = L.u_(L.not_(loc[i + 1]), loc[i])
            f2.append(f)
        f2 = L.and_(f2)

        new_formula = L.and_([f1, f2])

        super().__init__(formula=(new_formula, new_typeset))


class StrictOrderedVisit(CoreMovement):
    """Given a set of locations the robot should visit all the locations."""

    def __init__(self, ls: Union[Atom, Boolean, List[Atom], List[Boolean]] = None):
        new_typeset, loc = CoreMovement.process_input(ls)

        new_typeset, loc = CoreMovement.process_input(ls)
        lor = list(loc)
        lor.reverse()
        n = len(loc)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in loc:
            f.append(L.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        f1 = L.and_(f)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(loc[:n - 1]):
            f = L.u_(L.not_(loc[i + 1]), loc[i])
            f2.append(f)
        f2 = L.and_(f2)

        f3 = []
        """1..n-1   !l_{i} U l_{i} & X(!l_{i} U l_{i+1})"""
        for i, l in enumerate(loc[:n - 1]):
            f = L.u_(L.not_(loc[i]), L.and_([loc[i], L.x_(L.u_(L.not_(loc[i]), loc[i + 1]))]))
            f3.append(f)
        f3 = L.and_(f3)

        new_formula = L.and_([f1, f2, f3])

        super().__init__(formula=(new_formula, new_typeset))


if __name__ == '__main__':
    # op = Visit([Boolean("a"), Boolean("b"), Boolean("c")])
    op = StrictOrderedVisit([Boolean("k3"), Boolean("h2"), Boolean("e1")])

    print(op)
    print("ciao")
