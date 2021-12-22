import os

from custom_world import CustomWorld

from core.cgg import Node
from core.cgg.exceptions import CGGException
from core.specification.__legacy.formula.patterns.robotics.coremovement.surveillance import (
    StrictOrderedPatrolling,
)
from core.specification.__legacy.formula.patterns.robotics.trigger.triggers import (
    BoundDelay,
    BoundReaction,
)
from tools.persistence import Persistence

output_folder_path = (
    f"{Persistence.default_folder_path}/examples/{os.path.basename(os.getcwd())}"
)

"""We import the world"""
w = CustomWorld()

try:

    """Modeling the set of goals using robotic robotic.json."""
    set_of_goals = {
        Node(
            name="day_patrol_12",
            description="During context day => start from r1, patrol r1, r2 in strict order,\n"
            "Strict Ordered Patrolling Location r1, r2",
            context=w["day"],
            specification=StrictOrderedPatrolling([w["r1"], w["r2"]]),
            world=w,
        ),
        Node(
            name="night_patrol_34",
            description="During context night => start from r3, patrol r3, r4 in strict order,\n"
            "Strict Ordered Patrolling Location r3, r4",
            context=w["night"],
            specification=StrictOrderedPatrolling([w["r3"], w["r4"]]),
            world=w,
        ),
        Node(
            name="greet_person",
            description="Always => if see a person, greet in the same step,\n"
            "Only if see a person, greet immediately",
            specification=BoundReaction(w["person"], w["greet"]),
            world=w,
        ),
        Node(
            name="register_person",
            description="During context day => if see a person, register in the next step,\n"
            "Only if see a person, register in the next step",
            context=w["day"],
            specification=BoundDelay(w["person"], w["register"]),
            world=w,
        ),
    }

    """Save set of goals so that they can be loaded later"""
    Persistence.dump_goals(set_of_goals, output_folder_path)

except CGGException as e:
    raise e
