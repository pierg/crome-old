from cgg import Node
from cgg.exceptions import CGGException
from contract import Contract
from robocup.modeling_environement import RobocupHome
from robocup import output_folder_name
from specification.atom.pattern.basic import GF
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import *
from specification.formula import Formula
from tools.persistence import Persistence

"""We import the environment"""
w = RobocupHome()

"""if the robot has the object, then disable the sensor for new objects"""
no_objects_when_hold = PromptReaction(w["hold"], ~w["object_recognized"])

living_room = [w["l1"], w["l2"], w["l3"], w["l4"], w["l5"], w["l6"]]
kitchen = [w["k1"], w["k2"]]

"""patrol living room"""
patrol_living_room = Patrolling(living_room)

"""patrol kitchen"""
patrol_kitchen = Patrolling(kitchen)

"""if the robot is available to hold and its in the location where it recognises an object 
then it should not move from that location"""
stay_location_if_object = Formula("TRUE")
for loc in living_room:
    stay_location_if_object &= PromptReaction(w["object_recognized"] & ~w["hold"] & loc, ~w["object_recognized"])

"""Do not hold if no object is sensed"""
dont_hold_if_no_object = PromptReaction(~w["hold"] & ~w["object_recognized"], ~w["hold"])

"""If it drops the object then it does not hold anymore"""
if_drop_not_hold = PromptReaction(w["hold"] & w["drop"], ~w["hold"])

"""Drop only when it is in the garbage and is holding"""
drop_near_garbage = InstantaneousReaction(w["drop"], ~w["k3"] & w["hold"])

"""GF(!hold)"""
keep_free_hands = GF(~w["hold"])

try:

    """Modeling the set of goals using robotic robotic.json"""
    set_of_goals = {
        Node(name="cleanup",
             description="Inside the living room are some misplaced objects. "
                         "The robot has to tidy up that room, throwing to the garbage the unrecognized ones."
                         "Find all misplaced objects in a room and bring them to their predeﬁned locations.",
             context=w["housekeeping"] & w["cleanup"],
             specification=Contract(
                 assumptions=no_objects_when_hold,
                 guarantees=patrol_living_room &
                            stay_location_if_object &
                            dont_hold_if_no_object &
                            if_drop_not_hold &
                            drop_near_garbage &
                            keep_free_hands
             ),
             world=w_types),
        Node(name="gpse",
             description="General Purpose Service Robot."
                         "Similar to a modern smart-speaker,"
                         "The robot can be asked to do anything and it immediately response with a voice notification",
             specification=Contract(
                 guarantees=BoundReaction(w["alexa"], w["reply"])
             ),
             world=w_types),
        Node(name="groceries",
             description="The robot stores groceries into a pantry shelf while paying attention"
                         " to sorting objects in their appropriate place, i.e. storing an apple next to other fruits.",
             context=w["housekeeping"] & w["groceries"],
             specification=Contract(
                 guarantees=patrol_kitchen &
                            PromptReaction(w["groceries_recognized"], w["store"] & w["k2"])
             ),
             world=w_types),
    }

    """Save set of goals so that they can be loaded later"""
    Persistence.dump_goals(set_of_goals, output_folder_name)

except CGGException as e:
    raise e
