from typing import List, Union
from specification.atom import Atom
from specification.atom.pattern.robotics.coremovement import CoreMovement
from specification.atom.pattern.robotics.trigger import Trigger
from tools.logic import Logic
from type import Boolean


class ConditionalVisit(CoreMovement):
    """Given a set of locations the robot should visit all the locations everytime the condition is satisfied"""

    def __init__(self, pre: Union[Atom, Boolean], ls: Union[Atom, Boolean, List[Atom], List[Boolean]] = None):
        new_typeset_a, loc = CoreMovement.process_input(ls)

        new_typeset_b, condition = Trigger.process_uni_input(pre)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in loc:
            f.append(Logic.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        new_formula = Logic.g_(Logic.implies_(condition, Logic.and_(f)))

        new_typeset = new_typeset_a | new_typeset_b

        super().__init__(formula=(new_formula, new_typeset))


if __name__ == '__main__':
    op = ConditionalVisit(Boolean("condition"), [Boolean("a"), Boolean("b"), Boolean("c")])
    print(op)
    print("ciao")
