import pickle

from examples.simple_example_care_center import folder_name
from tools.persistence import Persistence
from worlds.illustrative_example import IllustrativeExample

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet
"""

"""Load CGG"""
cgg = Persistence.load_cgg(folder_name)

"""Realize Specification and Transition Controllers indicating the Maximum Transition Time"""
cgg.realize_all(t_trans=3)

"""Save CGG"""
cgg.save()
Persistence.dump_cgg(cgg)

print(cgg)

