from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.specification.lformula import LTL


def __hash__(self: LTL):
    return hash(self.string)


def __str__(self: LTL):
    return self.string
