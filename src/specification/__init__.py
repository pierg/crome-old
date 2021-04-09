from __future__ import annotations
from abc import ABC, abstractmethod
from specification.enums import *
from specification.exceptions import NotSatisfiableException
from tools.logic import LogicTuple
from tools.nuxmv import Nuxmv
from tools.spot import Spot
from typeset import Typeset


class Specification(ABC):

    @property
    def string(self) -> str:
        return self.formula()[0]

    @property
    def typeset(self) -> Typeset:
        return self.formula()[1]

    def __hash__(self):
        return hash(self.string)

    def __str__(self):
        return self.string

    def translate_to_buchi(self, name: str, path: str = None):
        """Realize the specification into a Buchi automaton"""
        Spot.generate_buchi(self.string, name, path)

    """Abstract Operators, must be implemented can be conly confronted with equal subtypes"""

    @abstractmethod
    def formula(self) -> (str, Typeset):
        pass

    @property
    @abstractmethod
    def spec_kind(self) -> SpecKind:
        pass

    @abstractmethod
    def __and__(self, other: Specification) -> Specification:
        """self & other
        Returns a new Specification with the conjunction with other"""
        pass

    @abstractmethod
    def __or__(self, other: Specification) -> Specification:
        """self | other
        Returns a new Specification with the disjunction with other"""
        pass

    @abstractmethod
    def __invert__(self: Specification) -> Specification:
        """Returns a new Specification with the negation of self"""
        pass

    @abstractmethod
    def __rshift__(self, other: Specification) -> Specification:
        """>>
        Returns a new Specification that is the result of self -> other (implies)"""
        pass

    @abstractmethod
    def __lshift__(self, other: Specification) -> Specification:
        """<<
        Returns a new Specification that is the result of other -> self (implies)"""
        pass

    @abstractmethod
    def __iand__(self, other: Specification) -> Specification:
        """self &= other
        Modifies self with the conjunction with other"""
        pass

    @abstractmethod
    def __ior__(self, other: Specification) -> Specification:
        """self |= other
        Modifies self with the disjunction with other"""
        pass

    @abstractmethod
    def contains_rule(self, other: AtomKind = None) -> bool:
        pass

    """"Comparing Specifications"""

    def is_satisfiable(self) -> bool:

        sat_check_formula = self.formula()

        """If does not contain Mutex Rules already, extract them and check the satisfiability"""
        from specification.atom import Atom
        mutex_rules = Atom.extract_mutex_rules(self.typeset)
        if mutex_rules is not None:
            sat_check_formula = LogicTuple.and_([self.formula(), mutex_rules.formula()])

        return Nuxmv.check_satisfiability(sat_check_formula)

    def is_true(self) -> bool:

        return self.string == "TRUE"

    def is_false(self) -> bool:

        return self.string == "FALSE"

    def is_valid(self) -> bool:

        return Nuxmv.check_validity(self.formula())

    def __lt__(self, other: Specification):
        """self < other. True if self is a refinement but not equal to other"""
        return self.__le__(other) and self.__ne__(other)

    def __le__(self: Specification, other: Specification):
        """self <= other. True if self is a refinement of other"""
        if other.is_true():
            return True

        """Check if self -> other is valid, considering the refinement rules r"""
        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        from specification.atom import Atom
        refinement_rules = Atom.extract_refinement_rules(self.typeset | other.typeset)
        if refinement_rules is not None:
            # ref_check_formula = (self & refinement_rules) >> other
            ref_check_formula = LogicTuple.implies_(LogicTuple.and_([self.formula(), refinement_rules.formula()]), other.formula())
        else:
            # ref_check_formula = self >> other
            ref_check_formula = LogicTuple.implies_(self.formula(), other.formula())
        return Nuxmv.check_validity(ref_check_formula)

    def __gt__(self, other: Specification):
        """self > other. True if self is an abstraction but not equal to other"""
        return self.__ge__(other) and self.__ne__(other)

    def __ge__(self, other: Specification):
        """self >= other. True if self is an abstraction of other"""
        if self.is_true():
            return True

        """Check if other -> self is valid, considering the refinement rules r"""
        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        from specification.atom import Atom
        refinement_rules = Atom.extract_refinement_rules(self.typeset | other.typeset)
        if refinement_rules is not None:
            # ref_check_formula = (other & refinement_rules) << self
            ref_check_formula = LogicTuple.implies_(other.formula(), LogicTuple.and_([self.formula(), refinement_rules.formula()]))
        else:
            # ref_check_formula = other << self
            ref_check_formula = LogicTuple.implies_(other.formula(), self.formula())
        return Nuxmv.check_validity(ref_check_formula)

    def __eq__(self, other: Specification):
        """Check if self -> other and other -> self"""
        if self.string == other.string:
            return True
        else:
            not_self = ~self
            if not_self.string == other.string:
                return False
            return self.__le__(other) and self.__ge__(other)

    def __ne__(self, other: Specification):
        """Check if self -> other and other -> self"""
        return not self.__eq__(other)
