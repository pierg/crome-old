from __future__ import annotations

from specification.atom import Atom, AtomKind
from specification.formula import Formula, FormulaKind

from typing import Set, Dict, TypeVar

from tools.logic import Logic
from type import Types, Boolean
from typeset import Typeset

AllTypes = TypeVar('AllTypes', bound=Types)


class RefinementRulesAdapter(Formula):
    def __init__(self, supertypes: Dict[AllTypes, Set[AllTypes]]):
        super().__init__(atom=Atom("TRUE"), kind=FormulaKind.REFINEMENT_RULES)

        for key_type, set_super_types in supertypes.items():
            if isinstance(key_type, Boolean):
                for super_type in set_super_types:
                    f = Logic.g_(Logic.implies_(key_type.name, super_type.name))
                    t = Typeset({key_type, super_type})
                    new_atom = Atom(formula=(f, t), kind=AtomKind.REFINEMENT_RULE)
                    self.__iand__(new_atom)
