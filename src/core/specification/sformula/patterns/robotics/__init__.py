from typing import Tuple

from core.specification.formula.atom import AtomKind, Pattern
from core.typeset import Typeset


class RoboticPattern(Pattern):
    """General RoboticPatterns Class."""

    def __init__(self, formula: Tuple[str, Typeset] = None):
        super().__init__(formula=formula, kind=AtomKind.ROBOTICPATTERN)
