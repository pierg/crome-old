from core.crometypes import Boolean, CTypes


class Active(Boolean):
    def __init__(self):
        super().__init__("active")

    def to_atom(self, kind=None):
        from core.specification import Specification

        return super().to_atom(kind=Specification.Kind.Atom.ACTIVE)

    @property
    def kind(self):
        return CTypes.Kind.ACTIVE
