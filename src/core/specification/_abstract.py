from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.specification import AtomKind, Specification, SpecKind


@abstractmethod
def formula(self: "Specification") -> (str, "Typeset"):
    pass


@property
@abstractmethod
def spec_kind(self: "Specification") -> "SpecKind":
    pass


@abstractmethod
def __and__(self: "Specification", other: "Specification") -> "Specification":
    """self & other Returns a new Specification with the conjunction with
    other."""


@abstractmethod
def __or__(self: "Specification", other: "Specification") -> "Specification":
    """self | other Returns a new Specification with the disjunction with
    other."""


@abstractmethod
def __invert__(self: "Specification") -> "Specification":
    """Returns a new Specification with the negation of self."""


@abstractmethod
def __rshift__(self: "Specification", other: "Specification") -> "Specification":
    """>> Returns a new Specification that is the result of self -> other
    (implies)"""


@abstractmethod
def __lshift__(self: "Specification", other: "Specification") -> "Specification":
    """<< Returns a new Specification that is the result of other -> self
    (implies)"""


@abstractmethod
def __iand__(self: "Specification", other: "Specification") -> "Specification":
    """self &= other Modifies self with the conjunction with other."""


@abstractmethod
def __ior__(self: "Specification", other: "Specification") -> "Specification":
    """self |= other Modifies self with the disjunction with other."""


@abstractmethod
def contains_rule(self: "Specification", other: "AtomKind" = None) -> bool:
    pass
