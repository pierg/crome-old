from type import BoundedInteger, Boolean, TypeKinds


class ContextTime(BoundedInteger):

    def __init__(self, name: str = "time"):
        super().__init__(name, min_value=0, max_value=24)

    @property
    def kind(self):
        return TypeKinds.CONTEXT


class ContextBooleanTime(Boolean):

    def __init__(self, name: str = "time"):
        super().__init__(name)

    @property
    def kind(self):
        return TypeKinds.CONTEXT

    def to_atom(self):
        from specification.atom import Atom, AtomKind
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})), check=False, kind=AtomKind.CONTEXT)


class ContextLocation(Boolean):

    def __init__(self, name: str = "location"):
        super().__init__(name)

    @property
    def kind(self):
        return TypeKinds.CONTEXT

    def to_atom(self):
        from specification.atom import Atom, AtomKind
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})), check=False, kind=AtomKind.CONTEXT)


class ContextIdentity(Boolean):

    def __init__(self, name: str = "identity"):
        super().__init__(name)

    @property
    def kind(self):
        return TypeKinds.CONTEXT

    def to_atom(self):
        from specification.atom import Atom, AtomKind
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})), check=False, kind=AtomKind.CONTEXT)
