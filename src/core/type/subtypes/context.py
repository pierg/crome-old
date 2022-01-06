from core.type import Boolean, BoundedInteger, Types


class ContextInteger(BoundedInteger):
    def __init__(
        self,
        name: str = "integer_context",
        min_value: int = None,
        max_value: int = None,
    ):
        super().__init__(name, min_value=0, max_value=24)

    @property
    def kind(self):
        return Types.Kind.CONTEXT


class ContextBoolean(Boolean):
    def __init__(self, name: str = "boolean_context", mutex: str = None):
        super().__init__(name)

        self.mutex = mutex

    @property
    def kind(self):
        return Types.Kind.CONTEXT

    @property
    def mutex_group(self):
        return self.mutex

    def to_atom(self, kind=None):
        from core.specification import Specification

        return super().to_atom(kind=Specification.Kind.CONTEXT)


class ContextIntegerTime(ContextInteger):
    def __init__(self, name: str = "time"):
        super().__init__(name, min_value=0, max_value=24)


class ContextBooleanTime(ContextBoolean):
    def __init__(self, name: str = "time"):
        super().__init__(name)


class ContextBooleanMode(ContextBoolean):
    def __init__(self, name: str = "mode"):
        super().__init__(name)


class ContextLocation(ContextBoolean):
    def __init__(self, name: str = "location"):
        super().__init__(name)


class ContextIdentity(ContextBoolean):
    def __init__(self, name: str = "identity"):
        super().__init__(name)
