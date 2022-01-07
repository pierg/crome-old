from core.crometypes import Boolean, Types


class Active(Boolean):
    def __init__(self):
        super().__init__("active")

    def to_atom(self, kind=None):
        from core.specification import Specification

        return super().to_atom(kind=Specification.Kind.ACTIVE_SIGNAL)

    @property
    def kind(self):
        return Types.Kind.ACTIVE
