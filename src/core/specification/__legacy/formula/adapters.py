from __future__ import annotations

from typing import Dict, Set, TypeVar

from core.crometypes import Boolean, Types
from core.specification.__legacy.atom import Atom, AtomKind
from core.specification.__legacy.formula import Formula, FormulaKind
from core.typeset import Typeset
from tools.logic import Logic

AllTypes = TypeVar("AllTypes", bound=Types)


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
