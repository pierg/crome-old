from tools.persistence import Persistence

folder_name = "running_example"


"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet in the next step
"""

"""Load CGG"""
cgg = Persistence.load_cgg(folder_name)

run = cgg.orchestrate(n_steps=50, t_min_context=6)
print(run)

