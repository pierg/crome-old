from typing import TYPE_CHECKING

from core.typeset import Typeset

if TYPE_CHECKING:
    from core.specification import Specification


@property
def string(self: "Specification") -> str:
    return self.formula()[0]


@property
def typeset(self: "Specification") -> Typeset:
    return self.formula()[1]
