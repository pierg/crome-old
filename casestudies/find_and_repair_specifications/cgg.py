from casestudies.find_and_repair_specifications.goals import set_of_goals
from core.cgg import Node

cgg = Node.build_cgg(set_of_goals)
print(cgg)
