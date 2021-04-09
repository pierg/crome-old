from contract import Contract
from cgg import Node
from cgg.exceptions import CGGException
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from type.subtypes.context import ContextBooleanTime
from type.subtypes.locations import ReachLocation

"""Continuation of 5_modelling_problems:
GOAL to model:
while 'day' is true => continuously visit the office, 
and while 'night' is true => continuously visit the bed
"""

"""Let us define 'day' and 'night' as Context instead"""


class Day(ContextBooleanTime):

    def __init__(self, name: str = "day"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "time"


class Night(ContextBooleanTime):

    def __init__(self, name: str = "night"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "time"


day = Day().to_atom()
night = Night().to_atom()

"""Our goals as before, using the Patrolling Pattern"""


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
patrol_bed = Patrolling([Bed()])

"""Infinitely Often Visit the Office =  GF(office) """
patrol_office = Patrolling([Office()])

try:

    n1 = Node(name="awake_during_day",
              context=day,
              specification=Contract(guarantees=patrol_bed))

    n2 = Node(name="sleep_during_night",
              context=night,
              specification=Contract(guarantees=patrol_office))

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "case_3b_context"

    cgg.translate_all_to_buchi()
    cgg.realize_specification_controllers()
    cgg.save()

    print(cgg)

    print("Although its satisfiable and realizable it does not reflect what we wat i.e.:"
          "when 'day' is true => continuously visit the office, "
          "and when 'night' is true => continuously visit the bed")

except CGGException as e:
    raise e
