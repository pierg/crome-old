from enum import Enum, auto
from typing import Dict

from core.patterns.robotics.coremovement import CoreMovement
from tools.logic import Logic


class Coverage(CoreMovement):
    class Kinds(Enum):
        VISIT = (auto(),)
        ORDERED_VISIT = auto()
        STRICT_ORDERED_VISIT = auto()

    patterns: Dict[Kinds, str] = {
        Kinds.VISIT: "Given a set of locations the robot should visit all the locations.",
        Kinds.ORDERED_VISIT: "Given a set of locations the robot should visit all the locations.",
        Kinds.STRICT_ORDERED_VISIT: "Given a set of locations the robot should visit all the locations.",
    }

    def __init__(self, formula: str, kind: Kinds):
        self.__formula: str = formula
        self.__kind: Coverage.Kinds = kind
        super().__init__(formula, CoreMovement.Kinds.COVERAGE)

    @staticmethod
    def check_inputs(*locations):
        for l in locations:
            if not isinstance(l, str):
                raise AttributeError


class Visit(Coverage):
    def __init__(self, *locations):
        Coverage.check_inputs(locations)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in locations:
            f.append(Logic.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        new_formula = Logic.and_(f)

        super().__init__(formula=new_formula, kind=Coverage.Kinds.VISIT)


class OrderedVisit(Coverage):
    """Given a set of locations the robot should visit all the locations."""

    def __init__(self, *locations):
        Coverage.check_inputs(locations)

        lor = list(locations)
        lor.reverse()
        n = len(locations)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in locations:
            f.append(Logic.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        f1 = Logic.and_(f)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(locations[: n - 1]):
            f = Logic.u_(Logic.not_(locations[i + 1]), locations[i])
            f2.append(f)
        f2 = Logic.and_(f2)

        new_formula = Logic.and_([f1, f2])

        super().__init__(formula=new_formula, kind=Coverage.Kinds.ORDERED_VISIT)


class StrictOrderedVisit(Coverage):
    def __init__(self, *locations):
        Coverage.check_inputs(locations)

        lor = list(locations)
        lor.reverse()
        n = len(locations)

        f = []

        """F(l1), F(l2), ...,F(ln)"""
        for l in locations:
            f.append(Logic.f_(l))

        """F(l1) & F(l2) & ... & F(ln)"""
        f1 = Logic.and_(f)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(locations[: n - 1]):
            f = Logic.u_(Logic.not_(locations[i + 1]), locations[i])
            f2.append(f)
        f2 = Logic.and_(f2)

        f3 = []
        """1..n-1   !l_{i} U l_{i} & X(!l_{i} U l_{i+1})"""
        for i, l in enumerate(locations[: n - 1]):
            f = Logic.u_(
                Logic.not_(locations[i]),
                Logic.and_(
                    [
                        locations[i],
                        Logic.x_(Logic.u_(Logic.not_(locations[i]), locations[i + 1])),
                    ]
                ),
            )
            f3.append(f)
        f3 = Logic.and_(f3)

        new_formula = Logic.and_([f1, f2, f3])

        super().__init__(formula=new_formula, kind=Coverage.Kinds.STRICT_ORDERED_VISIT)
