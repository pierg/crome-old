from enum import Enum, auto
from typing import Dict

from core.patterns.robotics.coremovement import CoreMovement
from tools.logic import Logic


class Surveillance(CoreMovement):
    class Kinds(Enum):
        PATROLLING = auto()
        ORDERED_PATROLLING = auto()
        STRICT_ORDERED_PATROLLING = auto()

    patterns: Dict[Kinds, str] = {
        Kinds.PATROLLING: "Keep visiting a set of locations, but not in a particular order.",
        Kinds.ORDERED_PATROLLING: "This patterns requires a robot to keep visiting a set of locations, in some specified order, similarly to sequenced patrolling. However, given an order, e.g., 1 and 2 between two locations, it is not admitted to the robot to visit 2 before 1.",
        Kinds.STRICT_ORDERED_PATROLLING: "Ordered patrolling patterns does not avoid a predecessor location to be visited multiple times before its successor. Strict Ordered Patrolling ensures that, after a predecessor is visited, it is not visited again before its successor.",
    }

    def __init__(self, formula: str, kind: Kinds):
        self.__formula: str = formula
        self.__kind: Surveillance.Kinds = kind
        super().__init__(formula, Surveillance.Kinds.SURVEILLANCE)

    @staticmethod
    def check_inputs(*locations):
        for l in locations:
            if not isinstance(l, str):
                raise AttributeError


class Patrolling(Surveillance):
    def __init__(self, *locations):
        Surveillance.check_inputs(locations)

        f = []

        for l in locations:
            f.append(Logic.gf_(l))

        super().__init__(formula=Logic.and_(f), kind=Surveillance.Kinds.PATROLLING)


class OrderedPatrolling(Surveillance):
    def __init__(self, *locations):
        Surveillance.check_inputs(locations)

        lor = list(locations)
        lor.reverse()
        n = len(locations)

        f1 = Logic.f_(lor[0])

        if len(locations) == 1:
            super().__init__(
                formula=Logic.g_(f1), kind=Surveillance.Kinds.ORDERED_PATROLLING
            )
            return

        """GF(l1 & F(l2 & ... F(ln))))"""
        for l in lor[1:]:
            f2 = Logic.and_([l, f1])
            f1 = Logic.f_(f2)
        f1 = Logic.g_(f1)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(locations[: n - 1]):
            f = Logic.u_(Logic.not_(locations[i + 1]), locations[i])
            f2.append(f)
        f2 = Logic.and_(f2)

        f3 = []
        """1..n   G(l_{(i+1)%n} -> X((!l_{(i+1)%n} U l_{i})))"""
        for i, l in enumerate(locations):
            f = Logic.g_(
                Logic.implies_(
                    locations[(i + 1) % n],
                    Logic.x_(
                        Logic.u_(Logic.not_(locations[(i + 1) % n]), locations[i])
                    ),
                )
            )
            f3.append(f)
        f3 = Logic.and_(f3)

        new_formula = Logic.and_([f1, f2, f3])

        super().__init__(
            formula=new_formula, kind=Surveillance.Kinds.ORDERED_PATROLLING
        )


class StrictOrderedPatrolling(Surveillance):
    """Ordered patrolling patterns does not avoid a predecessor location to be
    visited multiple times before its successor.

    Strict Ordered Patrolling ensures that, after a predecessor is
    visited, it is not visited again before its successor.
    """

    def __init__(self, *locations):

        Surveillance.check_inputs(locations)

        lor = list(locations)
        lor.reverse()
        n = len(locations)

        f1 = Logic.f_(lor[0])

        if len(locations) == 1:
            super().__init__(
                formula=Logic.g_(f1), kind=Surveillance.Kinds.STRICT_ORDERED_PATROLLING
            )
            return

        """GF(l1 & F(l2 & ... F(ln))))"""
        for l in lor[1:]:
            f2 = Logic.and_([l, f1])
            f1 = Logic.f_(f2)
        f1 = Logic.g_(f1)

        f2 = []
        """1..n-1   !l_{i+1} U l_{i}"""
        for i, l in enumerate(locations[: n - 1]):
            f = Logic.u_(Logic.not_(locations[i + 1]), locations[i])
            f2.append(f)
        f2 = Logic.and_(f2)

        f3 = []
        """1..n   G(l_{(i+1)%n} -> X((!l_{(i+1)%n} U l_{i})))"""
        for i, l in enumerate(locations):
            f = Logic.g_(
                Logic.implies_(
                    locations[(i + 1) % n],
                    Logic.x_(
                        Logic.u_(Logic.not_(locations[(i + 1) % n]), locations[i])
                    ),
                )
            )
            f3.append(f)
        f3 = Logic.and_(f3)

        if len(locations) > 2:
            f4 = []
            """1..n   G(l_{(i+1)%n} -> X((!l_{(i+1)%n} U l_{i})))"""
            for i, l in enumerate(locations):
                f = Logic.g_(
                    Logic.implies_(
                        locations[i],
                        Logic.x_(
                            Logic.u_(Logic.not_(locations[i]), locations[(i + 1) % n])
                        ),
                    )
                )
                f4.append(f)
            f4 = Logic.and_(f4)
            new_formula = Logic.and_([f1, f2, f3, f4])
        else:
            new_formula = Logic.and_([f1, f2, f3])

        super().__init__(
            formula=new_formula, kind=Surveillance.Kinds.STRICT_ORDERED_PATROLLING
        )
