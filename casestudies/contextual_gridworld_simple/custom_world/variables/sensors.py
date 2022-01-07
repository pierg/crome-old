from core.crometypes.subtypes.sensor import BooleanSensor


class Person(BooleanSensor):
    def __init__(self, name: str = "person"):
        super().__init__(name)
