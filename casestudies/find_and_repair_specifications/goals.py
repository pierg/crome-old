from casestudies.find_and_repair_specifications.world import StoreWorld
from core.cgg import Node
from core.contract import Contract
from core.patterns.basic import GF
from core.patterns.robotics.coremovement.surveillance import (
    Patrolling,
    StrictOrderedPatrolling,
)
from core.patterns.robotics.trigger import (
    BoundReaction,
    InstantaneousReaction,
    PromptReaction,
)
from core.specification.lformula import LTL

w = StoreWorld()


n1 = Node(
    name="day_patrolling",
    description="During the day keep visiting the `front' locations",
    context=w["dy"],
    specification=Contract(
        assumptions=None, guarantees=LTL(Patrolling("lf"), w.typeset)
    ),
    world=w,
)

set_of_goals = {
    Node(
        name="day_patrolling",
        description="During the day keep visiting the `front' locations",
        context=w["dy"],
        specification=Contract(
            assumptions=None, guarantees=LTL(Patrolling("lf"), w.typeset)
        ),
        world=w,
    ),
    Node(
        name="day_wave",
        description="During the day wave when seeing a person",
        specification=Contract(
            assumptions=LTL(GF("ps"), w.typeset),
            guarantees=LTL(BoundReaction("ps", "wa"), w.typeset),
        ),
        world=w,
    ),
    Node(
        name="night_patrolling",
        description="During the night patrol in order all the locations in a strict order",
        context=w["nt"],
        specification=Contract(
            assumptions=None,
            guarantees=LTL(StrictOrderedPatrolling("l1", "l2", "l4", "l3"), w.typeset),
        ),
        world=w,
    ),
    Node(
        name="night_report",
        description="During the night promptly send a report when in the back of the store",
        context=w["nt"],
        specification=Contract(
            assumptions=LTL(GF("lb"), w.typeset),
            guarantees=LTL(PromptReaction("lb", "re"), w.typeset),
        ),
        world=w,
    ),
    Node(
        name="night_charge",
        description="During the night, when in the store front, go promptly charging in the charging location",
        specification=Contract(
            assumptions=LTL(GF("lc"), w.typeset),
            guarantees=LTL(PromptReaction("lf", "lc & ch"), w.typeset),
        ),
        world=w,
    ),
    Node(
        name="always_picture",
        description="Always take a picture when seeing a person",
        specification=Contract(
            assumptions=LTL(GF("ps"), w.typeset),
            guarantees=LTL(InstantaneousReaction("ps", "pc"), w.typeset),
        ),
        world=w,
    ),
}


set_of_goalski = {
    Node(
        name="day_patrolling",
        description="During the day keep visiting the `front' locations",
        context=w["dy"],
        specification=Contract(
            assumptions=None, guarantees=LTL(Patrolling("l2"), w.typeset)
        ),
        world=w,
    ),
    Node(
        name="wave",
        description="During the day keep visiting the `front' locations",
        context=w["dy"],
        specification=Contract(
            assumptions=LTL(GF("ps"), w.typeset),
            guarantees=LTL(BoundReaction("ps", "wa"), w.typeset),
        ),
        world=w,
    ),
    Node(
        name="day_wave",
        description="During the day wave when seeing a person",
        context=w["nt"],
        specification=Contract(
            guarantees=LTL(Patrolling("l1"), w.typeset),
        ),
        world=w,
    ),
}
