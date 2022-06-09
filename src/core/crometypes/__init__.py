from __future__ import annotations

from abc import ABC
from enum import Enum, auto

"""Template Pattern"""

BASE_CLASS_TYPES = [
    "Boolean",
    "BoundedInteger",
    "BooleanAction",
    "IntegerAction",
    "Active",
    "ContextTime",
    "ContextBooleanTime",
    "ContextLocation",
    "ContextIdentity",
    "ReachLocation",
    "IntegerSensor",
    "BooleanSensor",
]


class CTypes(ABC):
    class Kind(Enum):
        SENSOR = auto()
        LOCATION = auto()
        ACTION = auto()
        ACTIVE = auto()
        CONTEXT = auto()

    def __init__(self, name: str):
        self.__name: str = name

    def __str__(self):
        return self.__name

    def __le__(self, other: CTypes):
        return isinstance(self, type(other))

    @property
    def name(self) -> str:
        return self.__name

    def kind(self) -> CTypes.Kind:
        pass

    @property
    def controllable(self) -> bool:
        if (
            self.kind == CTypes.Kind.SENSOR
            or self.kind == CTypes.Kind.CONTEXT
            or self.kind == CTypes.Kind.ACTIVE
        ):
            return False
        return True

    def __eq__(self, other):
        if self.name == other.name and type(self).__name__ == type(other).__name__:
            if isinstance(self, BoundedInteger):
                if self.min == other.min and self.max == other.max:
                    return True
                else:
                    return False
            return True
        return False

    def __hash__(self):
        return hash(self.name + type(self).__name__)


class Boolean(CTypes):
    def __init__(self, name: str):
        super().__init__(name)

    def to_atom(self, kind=None):
        from core.specification.lformula import LTL
        return LTL(self.name, kind=kind)

    @property
    def mutex_group(self) -> str:
        return ""


class BoundedInteger(CTypes):
    def __init__(self, name: str, min_value: int, max_value: int):
        self.__min = min_value
        self.__max = max_value
        super().__init__(name)

    @property
    def min(self) -> int:
        return self.__min

    @property
    def max(self) -> int:
        return self.__max
