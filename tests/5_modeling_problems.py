from typing import Set

from contract import Contract
from cgg import Node
from cgg.exceptions import CGGException
from specification.atom.pattern.basic import Init, G, F
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from type.subtypes.actions import BooleanAction
from type.subtypes.locations import ReachLocation
from type.subtypes.sensors import BooleanSensor

"""Let's define two actions and sensors"""


class Sleep(BooleanAction):

    def __init__(self, name: str = "sleep"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "life"


class Awake(BooleanAction):

    def __init__(self, name: str = "awake"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "life"


class Day(BooleanSensor):

    def __init__(self, name: str = "day"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "time"


class Night(BooleanSensor):

    def __init__(self, name: str = "night"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "time"


"""We want to model a CGG that :
'always sleep during the night and always awake during the day"""

day = Day().to_atom()
night = Night().to_atom()

sleep_now = Init(Sleep())
awake_now = Init(Awake())

"""CASE 1"""
try:

    n1 = Node(name="awake_during_day",
              specification=Contract(assumptions=day, guarantees=awake_now))

    n2 = Node(name="sleep_during_night",
              specification=Contract(assumptions=night, guarantees=sleep_now))

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "case_1"

    cgg.translate_all_to_buchi()
    cgg.realize_specification_controllers()
    cgg.save()

    print(cgg)

    print("The CGG  is realizable but it does not reflect the behaviour that we want")


except CGGException as e:
    raise e

"""CASE 2: Adding Globally in the assumptions"""
try:

    n1 = Node(name="awake_during_day",
              specification=Contract(assumptions=G(day), guarantees=awake_now))

    n2 = Node(name="sleep_during_night",
              specification=Contract(assumptions=G(night), guarantees=sleep_now))

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "case_2"

    cgg.translate_all_to_buchi()
    cgg.realize_specification_controllers()
    cgg.save()

    print(cgg)

    print("The CGG is realizable but it does not reflect the behaviour that we want"
          "since once is day/night then it has always to be day/night => no switch possible")


except CGGException as e:
    raise e

"""CASE 3: Adding Globally in the assumptions"""
try:

    n1 = Node(name="awake_during_day",
              specification=Contract(guarantees=G(day >> awake_now)))

    n2 = Node(name="sleep_during_night",
              specification=Contract(guarantees=G(night >> sleep_now)))

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "case_3"

    cgg.translate_all_to_buchi()
    cgg.realize_specification_controllers()
    cgg.save()

    print(cgg)

    print("In this case it works, does this approach work with any guarantees?")

except CGGException as e:
    raise e

"""CASE 3b: Adding Globally in the assumptions with different pattern"""


class Bed(ReachLocation):

    def __init__(self, name: str = "bed"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "locations"


class Office(ReachLocation):

    def __init__(self, name: str = "office"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "locations"


"""Infinitely Often Visit the Bed =  GF(bed) """
bed = Patrolling([Bed()])

"""Infinitely Often Visit the Office =  GF(office) """
office = Patrolling([Office()])

try:

    n1 = Node(name="awake_during_day",
              specification=Contract(guarantees=G(day >> office)))

    n2 = Node(name="sleep_during_night",
              specification=Contract(guarantees=G(night >> bed)))

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "case_3b"

    cgg.translate_all_to_buchi()
    cgg.realize_specification_controllers()
    cgg.save()

    print(cgg)

    print("Although its satisfiable and realizable it does not reflect what we want i.e.:"
          "when 'day' is true => continuously visit the office, "
          "and when 'night' is true => continuously visit the bed")

except CGGException as e:
    raise e
