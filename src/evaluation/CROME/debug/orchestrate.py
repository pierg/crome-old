from tools.persistence import Persistence

folder_name = "crome_evaluation"

cgg = Persistence.load_cgg(folder_name)

"""Launch a simulation of n_steps where each contexts does change for at least t_min_context """
run = cgg.orchestrate(n_steps=50, t_min_context=6)
print(run)
