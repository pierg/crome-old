from type.subtypes.actions import *


class Greet(BooleanAction):

    def __init__(self, name: str = "greet"):
        super().__init__(name)


class Cure(BooleanAction):

    def __init__(self, name: str = "cure"):
        super().__init__(name)
