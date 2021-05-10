from type.subtypes.sensor import *


class Person(BooleanSensor):

    def __init__(self, name: str = "person"):
        super().__init__(name)

