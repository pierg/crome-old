from typing import TYPE_CHECKING

from tools.logic import LogicTuple
from tools.nuxmv import Nuxmv

if TYPE_CHECKING:
    from core.specification import Specification


def is_satisfiable(self: "Specification") -> bool:
    if self.string == "TRUE":
        return True

    if self.string == "FALSE":
        return False

    sat_check_formula = self.formula()

    """If does not contain Mutex Rules already, extract them and check the satisfiability"""
    from core.specification.formula.atom import Atom

    mutex_rules = Atom.extract_mutex_rules(self.typeset)
    if mutex_rules is not None:
        sat_check_formula = LogicTuple.and_([self.formula(), mutex_rules.formula()])

    return Nuxmv.check_satisfiability(sat_check_formula)


def is_valid(self: "Specification") -> bool:
    if self.string == "TRUE":
        return True

    if self.string == "FALSE":
        return False

    return Nuxmv.check_validity(self.formula())


# TODO: REMOVE
def is_true(self: "Specification") -> bool:
    return self.string == "TRUE"


def is_false(self: "Specification") -> bool:
    return self.string == "FALSE"
