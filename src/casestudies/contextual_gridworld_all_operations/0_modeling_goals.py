from core.cgg import Node
from core.cgg.exceptions import CGGException
from custom_world import CustomWorld
from core.specification.atom.pattern.robotics.coremovement.surveillance import *
from core.specification.atom.pattern.robotics.trigger.triggers import *
from tools.persistence import Persistence

import os
output_folder_path = f"{Persistence.default_folder_path}/examples/{os.path.basename(os.getcwd())}"

"""We import the world"""
w = CustomWorld()

try:

    """Modeling the set of goals using robotic robotic.json"""
    set_of_goals = {
        Node(name="day_patrol_12",
             description="During context day => start from r1, patrol r1, r2 in strict order,\n"
                         "Strict Ordered Patrolling Location r1, r2",
             context=w["day"],
             specification=StrictOrderedPatrolling([w["r1"], w["r2"]]),
             world=w),
        Node(name="night_patrol_34",
             description="During context night => start from r3, patrol r3, r4 in strict order,\n"
                         "Strict Ordered Patrolling Location r3, r4",
             context=w["night"],
             specification=StrictOrderedPatrolling([w["r3"], w["r4"]]),
             world=w),
        Node(name="take_picture",
             description="Take picture if movements is detected near the entrance location r5",
             specification=InstantaneousReaction(w["movement"] & w["r5"], w["picture"]),
             world=w),
        Node(name="always_return_entrance",
             description="Always return to the entrance r5",
             specification=Patrolling([w["r5"]]),
             world=w),
        Node(name="greet_person",
             description="Always => if see a person, greet in the same step,\n"
                         "Only if see a person, greet immediately",
             specification=BoundReaction(w["person"], w["greet"]),
             world=w),
        Node(name="register_person",
             description="During context day => if see a person, register in the next step,\n"
                         "Only if see a person, register in the next step",
             context=w["day"],
             specification=BoundDelay(w["person"], w["register"]),
             world=w)
    }

    """Save set of goals so that they can be loaded later"""
    Persistence.dump_goals(set_of_goals, output_folder_path)

except CGGException as e:
    raise e
