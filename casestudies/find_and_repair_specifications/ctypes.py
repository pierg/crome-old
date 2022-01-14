from core.crometypes.subtypes.action import BooleanAction
from core.crometypes.subtypes.context import ContextBooleanTime
from core.crometypes.subtypes.location import ReachLocation
from core.crometypes.subtypes.sensor import BooleanSensor

"""SENSORS"""


class Person(BooleanSensor):
    def __init__(self, name: str = "ps"):
        super().__init__(name)


"""ACTIONS"""


class Charge(BooleanAction):
    def __init__(self, name: str = "ch"):
        super().__init__(name)


class Report(BooleanAction):
    def __init__(self, name: str = "re"):
        super().__init__(name)


class Picture(BooleanAction):
    def __init__(self, name: str = "pc"):
        super().__init__(name)


class Wave(BooleanAction):
    def __init__(self, name: str = "wa"):
        super().__init__(name)


"""LOCATIONS"""


class Front(ReachLocation):
    def __init__(self, name: str = "lf"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "abstracted_locations"


class Back(ReachLocation):
    def __init__(self, name: str = "lb"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "abstracted_locations"


class L1(Front):
    def __init__(self, name: str = "l1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L2", "L3"}


class L2(Front):
    def __init__(self, name: str = "l2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L1", "L4"}


class Charging(L2):
    def __init__(self, name: str = "lc"):
        super().__init__(name)


class L3(Front):
    def __init__(self, name: str = "l3"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L1", "L4", "L5"}


class L4(Front):
    def __init__(self, name: str = "l4"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L2", "L3"}


class L5(Back):
    def __init__(self, name: str = "l5"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L3"}


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
