from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Set

from aenum import Enum, auto, skip

from core.typeset import Typeset


class SpecNotSATException(Exception):
    def __init__(self, formula: str):
        self.formula = formula


class Specification(ABC):
    class Kind(Enum):
        UNDEFINED = auto()

        @skip
        class Atom(Enum):
            ACTION = auto()
            SENSOR = auto()
            LOCATION = auto()
            CONTEXT = auto()
            ACTIVE = auto()

        @skip
        class Rule(Enum):
            REFINEMENT = auto()
            MUTEX = auto()
            ADJACENCY = auto()
            LIVENESS = auto()

    class OutputStr(Enum):
        ORIGINAL = auto()
        SIMPLIFIED = auto()
        CNF = auto()
        DNF = auto()
        SUMMARY = auto()

    def __init__(self, formula: str, typeset: Typeset):

        self.__formula = formula
        self.__typeset = typeset

    def __hash__(self: Specification):
        return hash(str(self))

    def __str__(self: Specification):
        return self.string

    @property
    @abstractmethod
    def string(self) -> str:
        pass

    @property
    def typeset(self) -> Typeset:
        return self.__typeset

    @property
    def cnf(self) -> List[Set[Specification]]:
        pass

    @property
    def dnf(self) -> List[Set[Specification]]:
        pass

    def represent(self, output_type: Specification.OutputStr) -> str:
        pass

    @abstractmethod
    def __and__(self: Specification, other: Specification) -> Specification:
        """self & other Returns a new Specification with the conjunction with
        other."""

    @abstractmethod
    def __or__(self: Specification, other: Specification) -> Specification:
        """self | other Returns a new Specification with the disjunction with
        other."""

    @abstractmethod
    def __invert__(self: Specification) -> Specification:
        """Returns a new Specification with the negation of self."""

    @abstractmethod
    def __rshift__(self: Specification, other: Specification) -> Specification:
        """>> Returns a new Specification that is the result of self -> other
        (implies)"""

    @abstractmethod
    def __iand__(self: Specification, other: Specification) -> Specification:
        """self &= other Modifies self with the conjunction with other."""

    @abstractmethod
    def __ior__(self: Specification, other: Specification) -> Specification:
        """self |= other Modifies self with the disjunction with other."""

    def saturate(self, saturation: Specification):
        pass

    @property
    @abstractmethod
    def is_satisfiable(self: Specification) -> bool:
        pass

    @property
    @abstractmethod
    def is_valid(self: Specification) -> bool:
        pass

    @property
    def is_true(self: Specification) -> bool:
        return self.is_valid

    @property
    def is_false(self: Specification) -> bool:
        return not self.is_satisfiable

    def __lt__(self, other: Specification):
        """self < other.

        True if self is a refinement but not equal to other
        """
        return self.__le__(other) and self.__ne__(other)

    def __le__(self: Specification, other: Specification):
        """self <= other.

        True if self is a refinement of other
        """
        """Check if (self -> other) is valid"""
        return (self >> other).is_valid

    def __gt__(self, other: Specification):
        """self > other.

        True if self is an abstraction but not equal to other
        """
        return self.__ge__(other) and self.__ne__(other)

    def __ge__(self, other: Specification):
        """self >= other.

        True if self is an abstraction of other
        """

        """Check if (other -> self) is valid"""
        return (other >> self).is_valid

        #
        # """Check if other -> self is valid, considering the refinement rules r"""
        # """((r & s1) -> s2) === r -> (s1 -> s2)"""
        # from core.specification.__legacy.atom import Atom
        #
        # rules = Atom.extract_refinement_rules(self.typeset | other.typeset)
        # if rules is not None:
        #     formula = LogicTuple.implies_(
        #         other.formula(),
        #         LogicTuple.and_([self.formula(), rules.formula()]),
        #     )
        # else:
        #     formula = LogicTuple.implies_(other.formula(), self.formula())
        # return Nuxmv.check_validity(formula)

    def __eq__(self, other: Specification):
        """Check if self -> other and other -> self."""
        if self.string == other.string:
            return True
        else:
            not_self = ~self
            if not_self.string == other.string:
                return False
            return self.__le__(other) and self.__ge__(other)

    def __ne__(self, other: Specification):
        """Check if self -> other and other -> self."""
        return not self.__eq__(other)
