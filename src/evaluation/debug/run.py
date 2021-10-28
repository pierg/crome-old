import os

from core.cgg import Node
from core.cgg.exceptions import CGGException
from running_example.modeling_environment import RunningExample
from core.specification.atom.pattern.robotics.coremovement.surveillance import *
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

try:

    n_day = Node(name="day_patrol_a",
                 context=w["day"],
                 specification=ordered_patrol_day,
                 world=w)

    n_night = Node(name="night_patrol_b",
                   context=w["night"],
                   specification=ordered_patrol_night,
                   world=w)

    t_cgg_start = time.time()
    cgg = Node.build_cgg({n_day, n_night})
    t_cgg_end = time.time()

    t_cgg = t_cgg_end - t_cgg_start

    cgg.set_session_name(folder_name)
    cgg.save()
    print(cgg)

    cgg.realize_all(t_trans=3)
    cgg.save()

    Persistence.dump_cgg(cgg)

    run = cgg.orchestrate(n_steps=50, t_min_context=6)
    print(run)



except CGGException as e:
    raise e
