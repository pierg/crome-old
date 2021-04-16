from type.subtypes.actions import *





class HoldObject(BooleanAction):

    def __init__(self, name: str = "hold"):
        super().__init__(name)



class DropObject(BooleanAction):

    def __init__(self, name: str = "drop"):
        super().__init__(name)
