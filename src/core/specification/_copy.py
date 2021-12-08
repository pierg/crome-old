from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.specification import Specification


def __deepcopy__(self: Specification, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        if "__spot" not in k:
            setattr(result, k, deepcopy(v, memo))
    result.spotfy()
    return result
