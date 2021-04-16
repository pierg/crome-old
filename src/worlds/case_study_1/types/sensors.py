from type.subtypes.sensors import *


class ObjectRecognized(BooleanSensor):

    def __init__(self, name: str = "object_recognized"):
        super().__init__(name)


class ObjectUnknown(BooleanSensor):

    def __init__(self, name: str = "object_unknown"):
        super().__init__(name)
