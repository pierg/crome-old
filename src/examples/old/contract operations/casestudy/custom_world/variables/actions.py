from core.type.subtypes.action import *


class Greet(BooleanAction):
    def __init__(self, name: str = "greet"):
        super().__init__(name)


class Register(BooleanAction):
    def __init__(self, name: str = "register"):
        super().__init__(name)


class Picture(BooleanAction):
    def __init__(self, name: str = "picture"):
        super().__init__(name)
