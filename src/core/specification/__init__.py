from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto

from core.typeset import Typeset


class SpecNotSATException(Exception):
    def __init__(self, formula: str):
        self.formula = formula


class Specification(ABC):
    class Kind(Enum):
        UNDEFINED = auto()
        ACTIVE_SIGNAL = auto()
        CONTEXT = auto()
        ATOM_ACTION = auto()
        ATOM_SENSOR = auto()
        ATOM_LOCATION = auto()
        MUTEX_RULE = auto()
        AJACENCY_RULE = auto()
        LIVENESS_RULE = auto()
        REFINEMENT_RULE = auto()

        class Rule(Enum):
            REFINEMENT = auto()
            MUTEX = auto()
            ADJACENCY = auto()
            LIVENESS = auto()

    def __init__(self, formula: str, typeset: Typeset):

        self.__formula = formula
        self.__typeset = typeset

    from ._str import __hash__, __str__  # noqa
    from ._utils import translate_to_buchi  # noqa

    @property
    @abstractmethod
    def original_formula(self) -> str:
        pass

    @property
    def formula(self) -> str:
        return self.__formula

    @property
    def typeset(self) -> Typeset:
        return self.__typeset

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
    def __lshift__(self: Specification, other: Specification) -> Specification:
        """<< Returns a new Specification that is the result of other -> self
        (implies)"""

    @abstractmethod
    def __iand__(self: Specification, other: Specification) -> Specification:
        """self &= other Modifies self with the conjunction with other."""

    @abstractmethod
    def __ior__(self: Specification, other: Specification) -> Specification:
        """self |= other Modifies self with the disjunction with other."""

    def saturate(self, saturation: Specification):
        pass

    @abstractmethod
    def is_satisfiable(self: Specification) -> bool:
        pass

    @abstractmethod
    def is_valid(self: Specification) -> bool:
        pass

    def is_true(self: Specification) -> bool:
        return self.string == "TRUE"

    def is_false(self: Specification) -> bool:
        return self.string == "FALSE"

    def __lt__(self, other: Specification):
        """self < other.

        True if self is a refinement but not equal to other
        """
        return self.__le__(other) and self.__ne__(other)

    def __le__(self: Specification, other: Specification):
        """self <= other.

        True if self is a refinement of other
        """
        if other.is_true():
            return True

        """Check if self -> other is valid, considering the refinement rules r"""
        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        if self.is_true():
            return True

        assert self.is_satisfiable() and other.is_satisfiable()

        """((r & s1) -> s2) === r -> (s1 -> s2)"""

        # print(self)
        # print(other)
        # print(f"({str(self)}) -> ({str(other)})")
        # print(self << other)

        return (self << other).is_valid()

    def __gt__(self, other: Specification):
        """self > other.

        True if self is an abstraction but not equal to other
        """
        return self.__ge__(other) and self.__ne__(other)

    def __ge__(self, other: Specification):
        """self >= other.

        True if self is an abstraction of other
        """
        if self.is_true():
            return True

        assert self.is_satisfiable() and other.is_satisfiable()

        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        return (self >> other).is_valid()

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
