from cgg import Node
from cgg.exceptions import CGGException
from robocup.house import RobocupHome
from running_example import output_folder_name
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import *
from tools.persistence import Persistence


"""After modeling the world, we import it"""
w = RobocupHome()

try:

    """G1) during context day => start from r1, patrol r1, r2 in strict order"""
    g1 = Node(name="day_patrol_12",
              description="Strict Ordered Patrolling Location r1, r2",
              context=w["day"],
              specification=StrictOrderedPatrolling([w["r1"], w["r2"]]),
              world=w)

    """G2) during context night => start from r3, patrol r3, r4 in strict order"""
    g2 = Node(name="night_patrol_34",
              description="Strict Ordered Patrolling Location r3, r4",
              context=w["night"],
              specification=StrictOrderedPatrolling([w["r3"], w["r4"]]),
              world=w)

    """G3) always => if see a person, greet in the same step"""
    g3 = Node(name="greet_person",
              description="Only if see a person, greet immediately",
              specification=BoundReaction(w["person"], w["greet"]),
              world=w)

    """G4) during context day => if see a person, register in the next step"""
    g4 = Node(name="register_person",
              description="Only if see a person, register in the next step",
              context=w["day"],
              specification=BoundDelay(w["person"], w["register"]),
              world=w)

    """Automatically build the CGG"""
    cgg = Node.build_cgg({g1, g2, g3, g4})
    print(cgg)

    """Setting the saving folder"""
    cgg.set_session_name(output_folder_name)
    """Save CGG as text file"""
    cgg.save()
    """Save CGG so that it can be loaded later"""
    Persistence.dump_cgg(cgg)


except CGGException as e:
    raise e
