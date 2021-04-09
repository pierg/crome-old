from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from typeset import Typeset

if TYPE_CHECKING:
    from specification.formula import Formula, Atom
    from typing import TypeVar

    Formula_types = TypeVar('Formula_types', bound=Formula)


class PropositionsException(Exception):
    def __init__(self, message: str):
        self.message = f"\n******PROPOSITIONS_EXCEPTION******\n{message}\n"
        print(self.message)


class NotSatisfiableException(PropositionsException):

    def __init__(self, conj_a: Formula, conj_b: Formula, rules: Atom = None):
        self.conj_a = conj_a
        self.conj_b = conj_b
        self.rules = rules
        if rules is not None:
            message = f"PHI_1:\t {self.conj_a.string}\n" \
                           f"PHI_2:\t {self.conj_b.string}\n" \
                           f"RULES:\t {self.rules.string}\n" \
                           f"PHI_1 & PHI_2 & RULES is inconsistent"
        else:
            message = f"PHI_1:\t {self.conj_a.string}\n" \
                           f"PHI_2:\t {self.conj_b.string}\n" \
                           f"PHI_1 & PHI_2 is inconsistent"

        super().__init__(message=message)


class AtomNotSatisfiableException(Exception):

    def __init__(self, formula: Tuple[str, Typeset]):
        self.formula = formula
