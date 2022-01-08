from core.cgg import Node
from core.goal import Goal
from core.patterns.robotics.coremovement.surveillance import Patrolling
from core.specification.lformula import LTL
from examples.types.create_world import ExampleWorld

"""We import the world"""
w = ExampleWorld()

patrolling_top = (
    Node(
        name="day_patrol_12",
        description="During context day => start from r1, patrol r1, r2 in strict order,\n"
        "Strict Ordered Patrolling Location r1, r2",
        specification=LTL(Patrolling("rt"), w.typeset),
        world=w,
    ),
)

patrolling_r1_r2 = (
    Goal(
        name="day_patrol_12",
        description="During context day => start from r1, patrol r1, r2 in strict order,\n"
        "Strict Ordered Patrolling Location r1, r2",
        specification=LTL(Patrolling("r1", "r2"), w.typeset),
        world=w,
    ),
)

assert patrolling_r1_r2 <= patrolling_top
