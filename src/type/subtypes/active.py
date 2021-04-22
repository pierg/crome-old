from typing import Set

from type import Boolean, TypeKinds


class Active(Boolean):

    def __init__(self):
        super().__init__("active")

    def to_atom(self):
        from specification.atom import Atom, AtomKind
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})), check=False, kind=AtomKind.ACTIVE)

    @property
    def kind(self):
        return TypeKinds.ACTIVE
