from type import BoundedInteger, Boolean, TypeKinds


class IntegerAction(BoundedInteger):

    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)

    @property
    def kind(self):
        return TypeKinds.ACTION


class BooleanAction(Boolean):

    def __init__(self,
                 name: str,
                 mutex: str = None):
        super().__init__(name)

        self.mutex = mutex

    @property
    def kind(self):
        return TypeKinds.ACTION

    def to_atom(self):
        from specification.atom import Atom, AtomKind
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})), check=False, kind=AtomKind.ACTION)

    @property
    def mutex_group(self):
        return self.mutex
