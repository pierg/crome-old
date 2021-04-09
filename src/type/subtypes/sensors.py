from type import BoundedInteger, Boolean, TypeKinds


class IntegerSensor(BoundedInteger):

    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)

    @property
    def kind(self):
        return TypeKinds.SENSOR


class BooleanSensor(Boolean):

    def __init__(self, name: str):
        super().__init__(name)

    def to_atom(self):
        from specification.atom import Atom, AtomKind
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})), check=False, kind=AtomKind.SENSOR)

    @property
    def kind(self):
        return TypeKinds.SENSOR
