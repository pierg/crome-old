from typing import Tuple
from specification.atom import AtomKind
from specification.atom.pattern import Pattern
from typeset import Typeset


class RoboticPattern(Pattern):
    """
    General RoboticPatterns Class
    """

    def __init__(self, formula: Tuple[str, Typeset] = None):
        super().__init__(
            formula=formula,
            kind=AtomKind.ROBOTICPATTERN)

