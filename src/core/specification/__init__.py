from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from tools.logic import LogicTuple
from tools.nuxmv import Nuxmv

if TYPE_CHECKING:
    from core.specification.enums import AtomKind, SpecKind
    from core.typeset import Typeset


class Specification(ABC):
    from ._checks import is_false, is_satisfiable, is_true, is_valid  # noqa
    from ._properties import string, typeset  # noqa
    from ._str import __hash__, __str__  # noqa
    from ._utils import translate_to_buchi  # noqa

    @abstractmethod
    def formula(self: Specification) -> tuple[str, Typeset]:
        pass

    @property
    @abstractmethod
    def spec_kind(self: Specification) -> SpecKind:
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
    def __lshift__(self: Specification, other: Specification) -> Specification:
        """<< Returns a new Specification that is the result of other -> self
        (implies)"""

    @abstractmethod
    def __iand__(self: Specification, other: Specification) -> Specification:
        """self &= other Modifies self with the conjunction with other."""

    @abstractmethod
    def __ior__(self: Specification, other: Specification) -> Specification:
        """self |= other Modifies self with the disjunction with other."""

    @abstractmethod
    def contains_rule(self: Specification, other: AtomKind = None) -> bool:
        pass

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
        from core.specification.atom import Atom

        refinement_rules = Atom.extract_refinement_rules(self.typeset | other.typeset)
        if refinement_rules is not None:
            # ref_check_formula = (self & refinement_rules) >> other
            ref_check_formula = LogicTuple.implies_(
                LogicTuple.and_([self.formula(), refinement_rules.formula()]),
                other.formula(),
            )
        else:
            # ref_check_formula = self >> other
            ref_check_formula = LogicTuple.implies_(self.formula(), other.formula())
        return Nuxmv.check_validity(ref_check_formula)

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

        """Check if other -> self is valid, considering the refinement rules r"""
        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        from core.specification.atom import Atom

        refinement_rules = Atom.extract_refinement_rules(self.typeset | other.typeset)
        if refinement_rules is not None:
            # ref_check_formula = (other & refinement_rules) << self
            ref_check_formula = LogicTuple.implies_(
                other.formula(),
                LogicTuple.and_([self.formula(), refinement_rules.formula()]),
            )
        else:
            # ref_check_formula = other << self
            ref_check_formula = LogicTuple.implies_(other.formula(), self.formula())
        return Nuxmv.check_validity(ref_check_formula)

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
