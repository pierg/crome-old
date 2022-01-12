from core.crometypes import Boolean, BoundedInteger, CTypes


class IntegerAction(BoundedInteger):
    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)

    @property
    def kind(self):
        return CTypes.Kind.ACTION


class BooleanAction(Boolean):
    def __init__(self, name: str, mutex: str = None):
        super().__init__(name)

        if mutex is None:
            self.mutex = ""

    @property
    def kind(self):
        return CTypes.Kind.ACTION

    def to_atom(self, kind=None):
        from core.specification import Specification

        return super().to_atom(kind=Specification.Kind.Atom.ACTION)

    @property
    def mutex_group(self):
        return self.mutex
