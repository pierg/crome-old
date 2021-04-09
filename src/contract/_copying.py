from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract

from copy import deepcopy


def __deepcopy__(self: Contract, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        if k == "_Contract__composed_by":
            if len(v) == 1 and self == next(iter(v)):
                setattr(result, k, {result})
            else:
                setattr(result, k, deepcopy(v))
        elif k == "_Contract__conjoined_by":
            if len(v) == 1 and self == next(iter(v)):
                setattr(result, k, {result})
            else:
                setattr(result, k, deepcopy(v))
        else:
            setattr(result, k, deepcopy(v))
    return result
