from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Formula

from copy import deepcopy


def __deepcopy__(self: Formula, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        if k == "_Formula__cnf":
            setattr(result, k, list(self.cnf))
        elif k == "_Formula__dnf":
            setattr(result, k, list(self.dnf))
        else:
            setattr(result, k, deepcopy(v))
    return result
