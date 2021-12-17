from core.specification.exceptions import NotSatisfiableException
from core.type import Boolean
from core.type.subtypes.action import BooleanAction
from core.type.subtypes.context import ContextBooleanTime
from core.type.subtypes.location import ReachLocation
from core.type.subtypes.sensor import BooleanSensor
from core.world import World

"""Generic Boolena Types"""


class A(Boolean):
    def __init__(self, name: str = "a"):
        super().__init__(name)


class B(Boolean):
    def __init__(self, name: str = "b"):
        super().__init__(name)


class C(Boolean):
    def __init__(self, name: str = "c"):
        super().__init__(name)


class D(Boolean):
    def __init__(self, name: str = "d"):
        super().__init__(name)


"""SENSORS"""


class Person(BooleanSensor):
    def __init__(self, name: str = "ps"):
        super().__init__(name)


class Movement(BooleanSensor):
    def __init__(self, name: str = "mv"):
        super().__init__(name)


"""ACTIONS"""


class Greet(BooleanAction):
    def __init__(self, name: str = "gr"):
        super().__init__(name)


class Register(BooleanAction):
    def __init__(self, name: str = "re"):
        super().__init__(name)


class Picture(BooleanAction):
    def __init__(self, name: str = "pc"):
        super().__init__(name)


"""LOCATIONS"""


class Rt(ReachLocation):
    def __init__(self, name: str = "rt"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "abstracted_locations"


class Rb(ReachLocation):
    def __init__(self, name: str = "rb"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "abstracted_locations"


class R1(Rt):
    def __init__(self, name: str = "r1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R2", "R5"}


class R2(Rt):
    def __init__(self, name: str = "r2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R1", "R5"}


class R3(Rb):
    def __init__(self, name: str = "r3"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R4", "R5"}


class R4(Rb):
    def __init__(self, name: str = "r4"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R3", "R5"}


class R5(ReachLocation):
    def __init__(self, name: str = "r5"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R1", "R2", "R3", "R4"}


"""CONTEXT"""


class Day(ContextBooleanTime):
    def __init__(self, name: str = "dy"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


class Night(ContextBooleanTime):
    def __init__(self, name: str = "nt"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


"""We can set the generic types to be actions, i.e. controllable outputs"""


class GenericWorld(World):
    def __init__(self):
        super().__init__(actions={A(), B(), C(), D()})


class CustomWorld(World):
    def __init__(self):
        super().__init__(
            actions={Picture(), Greet(), Register()},
            locations={R1(), R2(), R5(), R4(), R5()},
            sensors={Movement(), Person()},
            contexts={Day(), Night()},
        )


if __name__ == "__main__":
    """We can create instances of types."""
    person = Person()
    picture = Picture()

    """From the type we can produce an atomic proposition"""
    picture_ap = picture.to_atom()

    """Types can be mutually exclusive"""
    r1 = R1().to_atom()
    r2 = R2().to_atom()
    try:
        x = r1 & r2
    except NotSatisfiableException:
        print(f"{r1.string}, and {r2.string} are mutually exclusive!")

    x = r1 | r2

    print(x)
