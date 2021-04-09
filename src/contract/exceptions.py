from __future__ import annotations
from typing import TYPE_CHECKING, Set

from specification.exceptions import PropositionsException

if TYPE_CHECKING:
    from specification import Specification
    from contract import Contract
    from typing import TypeVar

    Formula_types = TypeVar('Formula_types', bound=Specification)


class ContractException(Exception):
    def __init__(self, message: str):
        self.message = f"\n******CONTRACT_EXCEPTION******\n{message}\n"
        print(self.message)


class IncompatibleContracts(ContractException):
    def __init__(self, contract: Contract, prop_ex: PropositionsException):
        self.contact = contract
        self.prop_ex = prop_ex
        message = f"A:\t {self.contact.assumptions.string}\n" \
                  f"A is inconsistent with the assumptions of the other contracts \t=> Contract Incompatible"
        super().__init__(message=message)


class InconsistentContracts(ContractException):
    def __init__(self, contract: Contract, prop_ex: PropositionsException):
        self.contact = contract
        self.prop_ex = prop_ex
        message = f"G:\t {self.contact.guarantees.string}\n" \
                  f"G is inconsistent with the guarantees of the other contracts \t=> Contract Inconsistent"
        super().__init__(message=message)


class UnfeasibleContracts(ContractException):
    def __init__(self, contract: Contract, prop_ex: PropositionsException):
        self.contact = contract
        self.prop_ex = prop_ex
        message = f"A:\t {self.contact.assumptions.string}\n" \
                  f"G:\t {self.contact.guarantees.string}\n" \
                  f"A & G is inconsistent \t=> Contract Inconsistent"
        super().__init__(message=message)

