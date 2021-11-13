from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.specification import Specification


def __hash__(self: Specification):
    return hash(self.string)


def __str__(self: Specification):
    return self.string
