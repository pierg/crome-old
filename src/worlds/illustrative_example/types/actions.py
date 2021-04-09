from type.subtypes.actions import *


class Greet(BooleanAction):

    def __init__(self, name: str = "greet"):
        super().__init__(name)
