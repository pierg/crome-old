from type.subtypes.action import *





class HoldObject(BooleanAction):

    def __init__(self, name: str = "hold"):
        super().__init__(name)



class DropObject(BooleanAction):

    def __init__(self, name: str = "drop"):
        super().__init__(name)


class PickupObject(BooleanAction):

    def __init__(self, name: str = "pickup"):
        super().__init__(name)
