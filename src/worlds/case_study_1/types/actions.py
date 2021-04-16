from type.subtypes.actions import *





class HoldObject(BooleanAction):

    def __init__(self, name: str = "hold"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "object_handling"


class DropObject(BooleanAction):

    def __init__(self, name: str = "drop"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "object_handling"
