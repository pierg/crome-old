from core.crometypes import Boolean, BoundedInteger, Types


class IntegerSensor(BoundedInteger):
    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)

    @property
    def kind(self):
        return Types.Kind.SENSOR


class BooleanSensor(Boolean):
    def __init__(self, name: str, mutex: str = None):
        super().__init__(name)

    def to_atom(self, kind=None):
        from core.specification import Specification

        return super().to_atom(kind=Specification.Kind.ATOM_SENSOR)

    @property
    def kind(self):
        return Types.Kind.SENSOR
