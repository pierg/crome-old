from typing import List, Union
from specification.atom import Atom
from specification.atom.pattern.robotics.coremovement import CoreMovement
from tools.logic import Logic
from type import Boolean


class Patrolling(CoreMovement):
    def __init__(self, ls: Union[List[Atom], List[Boolean]] = None):
        new_typeset, loc = CoreMovement.process_input(ls)
        f = []
        for l in loc:
            f.append(Logic.gf_(l))

        super().__init__(formula=(Logic.and_(f), new_typeset))

    """Keep visiting a set of locations, but not in a particular order."""


class OrderedPatrolling(CoreMovement):
    """This pattern requires a robot to keep visiting a set of locations, in some specified order,
    similarly to sequenced patrolling.
    However, given an order, e.g., 1 and 2 between two locations,
    it is not admitted to the robot to visit 2 before 1."""

    def __init__(self, ls: Union[List[Atom], List[Boolean]] = None):

        new_typeset, loc = CoreMovement.process_input(ls)
        lor = list(loc)
        lor.reverse()
        n = len(loc)

        f1 = Logic.f_(lor[0])

        if len(ls) == 1:
            super().__init__(formula=(Logic.g_(f1), new_typeset))
            return

        """GF(l1 & F(l2 & ... F(ln))))"""
        for l in lor[1:]:
            f2 = Logic.and_([l, f1])
            f1 = Logic.f_(f2)
        f1 = Logic.g_(f1)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(loc[:n - 1]):
            f = Logic.u_(Logic.not_(loc[i + 1]), loc[i])
            f2.append(f)
        f2 = Logic.and_(f2)

        f3 = []
        """1..n   G(l_{(i+1)%n} -> X((!l_{(i+1)%n} U l_{i})))"""
        for i, l in enumerate(loc):
            f = Logic.g_(Logic.implies_(loc[(i + 1) % n], Logic.x_(Logic.u_(Logic.not_(loc[(i + 1) % n]), loc[i]))))
            f3.append(f)
        f3 = Logic.and_(f3)

        new_formula = Logic.and_([f1, f2, f3])

        super().__init__(formula=(new_formula, new_typeset))


class StrictOrderedPatrolling(CoreMovement):
    """Ordered patrolling pattern does not avoid a predecessor location to be visited multiple times
    before its successor. Strict Ordered Patrolling ensures that, after a predecessor is visited,
    it is not visited again before its successor."""

    def __init__(self, ls: Union[List[Atom], List[Boolean]] = None):

        new_typeset, loc = CoreMovement.process_input(ls)
        lor = list(loc)
        lor.reverse()
        n = len(loc)

        f1 = Logic.f_(lor[0])

        if len(ls) == 1:
            super().__init__(formula=(Logic.g_(f1), new_typeset))
            return

        """GF(l1 & F(l2 & ... F(ln))))"""
        for l in lor[1:]:
            f2 = Logic.and_([l, f1])
            f1 = Logic.f_(f2)
        f1 = Logic.g_(f1)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(loc[:n - 1]):
            f = Logic.u_(Logic.not_(loc[i + 1]), loc[i])
            f2.append(f)
        f2 = Logic.and_(f2)

        f3 = []
        """1..n   G(l_{(i+1)%n} -> X((!l_{(i+1)%n} U l_{i})))"""
        for i, l in enumerate(loc):
            f = Logic.g_(Logic.implies_(loc[(i + 1) % n], Logic.x_(Logic.u_(Logic.not_(loc[(i + 1) % n]), loc[i]))))
            f3.append(f)
        f3 = Logic.and_(f3)

        f4 = []
        """1..n   G(l_{(i+1)%n} -> X((!l_{(i+1)%n} U l_{i})))"""
        for i, l in enumerate(loc):
            f = Logic.g_(Logic.implies_(loc[i], Logic.x_(Logic.u_(Logic.not_(loc[i]), loc[(i + 1) % n]))))
            f4.append(f)
        f4 = Logic.and_(f4)

        new_formula = Logic.and_([f1, f2, f3, f4])

        super().__init__(formula=(new_formula, new_typeset))


if __name__ == '__main__':
    op = OrderedPatrolling([Boolean("a"), Boolean("b"), Boolean("c")])
    print(op)
    print("ciao")
