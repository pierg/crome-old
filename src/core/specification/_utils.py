from typing import TYPE_CHECKING

from tools.spot import Spot

if TYPE_CHECKING:
    from core.specification import Specification


def translate_to_buchi(self: "Specification", name: str, path: str = None):
    """Realize the specification into a Buchi automaton."""
    Spot.generate_buchi(self.string, name, path)
