from typing import List, Tuple, Union

from core.specification.__legacy.formula import Atom, RoboticPattern
from core.type import Boolean
from core.typeset import Typeset


class CoreMovement(RoboticPattern):
    """Core Movements All the variables are locations where there robot can be
    at a certain time."""

    def __init__(self, formula: Tuple[str, Typeset] = None):
        super().__init__(formula=formula)

    @staticmethod
    def process_input(
        ls: Union[Atom, Boolean, List[Atom], List[Boolean]]
    ) -> Tuple[Typeset, List[str]]:

        new_typeset = Typeset()
        formulae_str = []

        if not isinstance(ls, list):
            ls = [ls]
        for i, elem in enumerate(ls):
            if isinstance(elem, Boolean):
                new_typeset |= elem
                formulae_str.append(elem.name)
            elif isinstance(elem, Atom):
                new_typeset |= elem.typeset
                formulae_str.append(elem.string)
            else:
                raise AttributeError

        return new_typeset, formulae_str
