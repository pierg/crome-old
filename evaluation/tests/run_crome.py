import os

from cgg import Node
from cgg.exceptions import CGGException
from running_example.modeling_environment import RunningExample
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import *
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

"""Only if see a person, greet immediately"""
greet = BoundReaction(w["person"], w["greet"])

"""Only if see a person, register in the next step"""
register = BoundDelay(w["person"], w["register"])

try:

    n_day = Node(name="day_patrol_a",
                 context=w["day"],
                 specification=ordered_patrol_day,
                 world=w)

    n_night = Node(name="night_patrol_b",
                   context=w["night"],
                   specification=ordered_patrol_night,
                   world=w)

    n_greet = Node(name="greet_person",
                   specification=greet,
                   world=w)

    n_register = Node(name="register_person",
                      context=w["day"],
                      specification=register,
                      world=w)

    t_cgg_start = time.time()
    cgg = Node.build_cgg({n_day, n_night, n_greet, n_register})
    t_cgg_end = time.time()

    t_cgg = t_cgg_end - t_cgg_start

    cgg.set_session_name(folder_name)
    cgg.save()
    print(cgg)

    cgg.realize_all(t_trans=3)

    t_s_controllers = 0
    n_s_controllers = 0
    states = []
    transitions = []
    for node in cgg.get_scenarios():
        t_s_controllers += node.synth_time
        n_s_controllers += 1
        states.append(str(len(node.controller.states)))
        transitions.append(str(len(node.controller.transitions)))

    t_t_controllers = 0
    n_t_controllers = 0
    for key, controller in cgg.t_controllers.items():
        t_t_controllers += controller.synth_time
        n_t_controllers += 1

    res = ""
    res += f"TIME CGG BUILD  \t= {t_cgg}\n"
    res += f"NUMBER OF S-CTRL\t= {n_s_controllers}\n"
    res += f"NUMBER OF STATES\t= {', '.join(states)}\n"
    res += f"NUMBER OF TRANSITIONS\t= {', '.join(transitions)}\n"
    res += f"\nNUMBER OF T-CTRL\t= {n_t_controllers}\n"
    res += f"TIME S-CTRL     \t= {t_s_controllers}\n"
    res += f"TIME T-CTRL     \t= {t_t_controllers}\n"
    res += f"TIME TOTAL      \t= {t_cgg + t_s_controllers + t_t_controllers}\n\n"

    print(f"\n\nRESULTS:\n{res}")

    """Launch a simulation of n_steps where each contexts does change for at least t_min_context """
    run = cgg.orchestrate(n_steps=50, t_min_context=6)
    print(run)

    Store.save_to_file(f"{res}", f"CROME/results.txt", absolute_folder_path=f"{path}")

    """Save simulation as text file"""
    Store.save_to_file(str(run), file_name="CROME/run.txt", absolute_folder_path=f"{path}")


except CGGException as e:
    raise e
