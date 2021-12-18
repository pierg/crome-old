from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.specification.sformula import Sformula


def __hash__(self: Sformula):
    return hash(self.string)


def __str__(self: Sformula):
    return self.string
