from examples.case_study_1 import folder_name
from cgg import Node
from cgg.exceptions import CGGException
from specification.atom.pattern.robotics.coremovement.coverage import Visit
from specification.atom.pattern.robotics.coremovement.coverage_new import ConditionalVisit
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import *
from tools.persistence import Persistence
from worlds.case_study_1 import CaseStudy

"""We import the world"""
w = CaseStudy()
ap = w.get_atoms()

living_room = [ap["l1"], ap["l2"], ap["l3"], ap["l4"], ap["l5"], ap["l6"]]
garbage = ap["k3"]

hold = ap["hold"]
drop = ap["drop"]
object_recognized = ap["object_recognized"]

example = ap["hold"] & ~ap["drop"] & ~ap["pickup"]
print(example)

patrol_living_room = Patrolling(living_room)
hold_recognized_object = PromptReaction(ap["object_recognized"], ap["hold"])
# hold_recognized_object = PromptReaction(ap["object_recognized"] & ~ap["hold"], ap["hold"])
# keep_holding_until_garbage = Wait(ap["hold"], ap["k3"])
visit_garbage_if_hold = ConditionalVisit(ap["hold"], ap["k3"])
# visit_garbage_if_hold = Visit(ap["k3"])
# drop_to_garbage = PromptReaction(ap["k3"], ap["drop"])
# drop_to_garbage = PromptReaction(ap["hold"] & ap["k3"], ap["drop"] & ~ap["hold"])

print(~ap["hold"])
cgg = Node(name="clean_up",
           specification=patrol_living_room &
                         hold_recognized_object &
                         # keep_holding_until_garbage &
                         visit_garbage_if_hold,
                         # drop_to_garbage,
           world=w)

cgg.set_session_name(folder_name)

cgg.realize_to_controller()

print(cgg)
