from tools.persistence import Persistence
from running_example import output_folder_name
from tools.storage import Store

"""Load CGG"""
cgg = Persistence.load_cgg(output_folder_name)

"""Launch a simulation of n_steps where each contexts does change for at least t_min_context """
run = cgg.orchestrate(n_steps=50, t_min_context=6)
print(run)

"""Save simulation as text file"""
Store.save_to_file(str(run), file_name="simulation.txt", output_folder_name=output_folder_name)
