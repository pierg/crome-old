from type.subtypes.context import ContextBooleanTime, ContextIdentity


class Day(ContextBooleanTime):

    def __init__(self, name: str = "day"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


class Night(ContextBooleanTime):

    def __init__(self, name: str = "night"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"




class Severe(ContextIdentity):

    def __init__(self, name: str = "severe"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "severe"
