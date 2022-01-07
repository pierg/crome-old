from casestudies.find_and_repair_specifications.world import StoreWorld
from core.cgg import Node
from core.patterns.robotics.coremovement.surveillance import (
    Patrolling,
    StrictOrderedPatrolling,
)
from core.patterns.robotics.trigger import BoundDelay, BoundReaction
from core.specification.lformula import LTL

w = StoreWorld()

set_of_goals = {
    Node(
        name="day_visit",
        description="During the day keep visiting the front of the store",
        context=w["dy"],
        specification=LTL(Patrolling("ft"), w.typeset),
        world=w,
    ),
    Node(
        name="always_picture",
        description="Always take a picture after seeing a person",
        specification=LTL(BoundDelay("ps", "pc"), w.typeset),
        world=w,
    ),
    Node(
        name="always_wave",
        description="Always immediately greet when seeing a person",
        specification=LTL(BoundReaction("ps", "gr"), w.typeset),
        world=w,
    ),
    Node(
        name="night_patrolling",
        description="During the night patrol in order all the locations of the store",
        context=w["nt"],
        specification=LTL(StrictOrderedPatrolling("l1", "l2", "l3", "l4"), w.typeset),
        world=w,
    ),
    Node(
        name="night_report",
        description="During the night send a report when in the back of the store",
        context=w["nt"],
        specification=LTL(BoundReaction("bk", "re"), w.typeset),
        world=w,
    ),
    Node(
        name="day_visit",
        description="During the night keep visiting the back of the store",
        context=w["dy"],
        specification=LTL(Patrolling("bk"), w.typeset),
        world=w,
    ),
}
