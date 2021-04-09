from __future__ import annotations

from typing import TYPE_CHECKING

from specification.formula import Formula, FormulaOutput

if TYPE_CHECKING:
    from contract import Contract


def __str__(self: Contract):
    """Override the print behavior"""
    ret = "\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    if isinstance(self.assumptions, Formula):
        ret += '  assumption'
        ret += '\n  DNF:\t' + self.assumptions.pretty_print(FormulaOutput.DNF) + ""
        ret += '\n  CNF:\t' + self.assumptions.pretty_print(FormulaOutput.CNF) + "\n"
    else:
        ret += '\n  ATM:\t' + str(self.assumptions) + "\n"

    if isinstance(self.guarantees, Formula):
        ret += '\n  guarantees'
        ret += '\n  DNF:\t' + self.guarantees.pretty_print(FormulaOutput.DNF) + ""
        ret += '\n  CNF:\t' + self.guarantees.pretty_print(FormulaOutput.CNF) + "\n"
    else:
        ret += '\n  ATM:\t' + str(self.guarantees) + "\n"
    ret += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

    return ret