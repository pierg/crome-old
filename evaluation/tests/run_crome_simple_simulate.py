import os

from cgg import Node
from cgg.exceptions import CGGException
from running_example.modeling_environment import RunningExample
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import *
from tools.persistence import Persistence
from tools.storage import Store
import time

folder_name = "crome_evaluation"

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet in the next step
"""

path = os.path.abspath(os.path.dirname(__file__))

"""We import the world"""
w = RunningExample()

"""Strict Ordered Patrolling Location r1, r2"""
ordered_patrol_day = StrictOrderedPatrolling([w["r1"], w["r2"]])

"""Strict Ordered Patrolling Location r3, r4"""
ordered_patrol_night = StrictOrderedPatrolling([w["r3"], w["r4"]])

# """Only if see a person, greet immediately"""
# greet = BoundReaction(w["person"], w["greet"])
#
# """Only if see a person, register in the next step"""
# register = BoundDelay(w["person"], w["register"])

try:

    cgg = Persistence.load_cgg(folder_name)

    """Launch a simulation of n_steps where each contexts does change for at least t_min_context """
    run = cgg.orchestrate(n_steps=50, t_min_context=6)
    print(run)

    """Save simulation as text file"""
    Store.save_to_file(str(run), file_name="crome_simple_run.txt", absolute_folder_path=f"{path}")


except CGGException as e:
    raise e
